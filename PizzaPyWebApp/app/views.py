from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.urls import reverse
from django.conf import settings
from urllib.parse import urlparse


# Create your views here.

# NAV LINK (PAGES)
def index(request):
    context = {}
    return render(request, "index.html", context)


def event_page(request, group_name=None):
    # return render(request, 'event_page.html')
    return get_upcoming_events(request, group_name)


def about_page(request):
    return render(request, "about_page.html")


# BASE URL SETUP
def get_redirect_uri(request):
    default_group_name = "pizzapy-ph"

    path = request.path.rstrip("/")
    parts = path.split("/")

    if len(parts) >= 3:
        if len(parts) == 3:  # URL is like /events/upcoming-events
            parts.append(default_group_name)  # Append default group name
        path_to_join = "/".join(parts)
        return request.build_absolute_uri(path_to_join)
    else:
        return None


# MEETUP TOKEN ACCESS
def get_access_token(request, code):
    REDIRECT_URI = get_redirect_uri(request)
    if not REDIRECT_URI:
        return None  # Unable to determine redirect URI

    token_url = "https://secure.meetup.com/oauth2/access"
    payload = {
        "client_id": settings.OAUTH_KEY,
        "client_secret": settings.OAUTH_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }

    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        return None


# FETCH EVENT VIA QUERY
def fetch_events(query, token, variables):

    url = "https://api.meetup.com/gql"
    headers = {"Authorization": "Bearer " + token}
    response = requests.post(
        url, json={"query": query, "variables": variables}, headers=headers
    )
    if response.status_code == 200:
        return response.json()
    else:
        return None


# EXTRACT EVENTS TO RENDER
def extract_events(data, event_timeline):
    return (
        data.get("data", {})
        .get("groupByUrlname", {})
        .get(event_timeline, {})
        .get("edges", [])
    )


# GET ALL UPCOMING EVENTS API
def get_upcoming_events(request, group_name=None):
    if not group_name:
        group_name = "pizzapy-ph"

    upcoming_events_query = """
    query ($urlname: String!) {
        groupByUrlname(urlname: $urlname) {
            id,
            upcomingEvents(input: { first: 3 }, sortOrder: ASC){
                count,
                pageInfo {
                    endCursor
                },
                edges {
                    node {
                        id
                        title
                        description
                        eventType
                        images {
                                source
                        }
                        venue {
                            address
                            city
                            postalCode
                        }
                        createdAt
                        dateTime
                        endTime
                        timezone
                        going
                        shortUrl
                        host {
                            name
                            username
                            email
                            memberPhoto {
                                id
                                baseUrl
                                preview
                                source
                            }
                            memberUrl
                            organizedGroupCount
                        }
                    }
                }
            }
        }
    }
    """
    token = request.token
    if not token:
        return HttpResponse("Failed to retrieve access token", status=400)

    variables = {"urlname": group_name}
    data = fetch_events(upcoming_events_query, token, variables)

    if data:
        events = extract_events(data, "upcomingEvents")
        # print(events)
        if events:
            first_event = events[0]["node"]
            other_events = [event["node"] for event in events[1:]]
            return render(
                request,
                "event_page.html",
                {"first_event": first_event, "other_events": other_events},
            )
        else:
            return render(
                request,
                "event_page.html",
                {"error_message": "No upcoming events found", "events_json": "[]"},
            )
    else:
        return render(
            request,
            "event_page.html",
            {"error_message": "Failed to retrieve events", "events_json": "[]"},
        )


# EVENT TOGGLE FROM PAST AND UPCOMING EVENTS
def event_dispatcher(request, event_timeline=None, group_name=None):
    if event_timeline == "past-events":
        return  # get_past_events(request, group_name)
    elif event_timeline == "upcoming-events":
        return get_upcoming_events(request, group_name)
    else:
        return HttpResponseNotFound("Event type not found")


# ATTEND EVENT VIA MEETUP API
def attend_event(request, event_id):
    if request.method == "POST":
        group_name = request.POST.get("group_name")
        return HttpResponseRedirect(reverse("get_upcoming_events", args=[group_name]))
    else:
        return HttpResponse(status=405)
