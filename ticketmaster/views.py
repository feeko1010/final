from datetime import datetime

# Make sure to install requests using 'pip install requests' on your terminal, otherwise 'requests' will not work
import requests
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import AddToFavoritesForm
from .models import FavoriteEvent


def search(request):
    # if the request method is a post
    if request.method == "POST":
        # get the search term and location
        classification = request.POST.get("classification")
        city = request.POST.get("city")
        apikey = "IiDX8bZGBAgaqzmNln5rvM5mFZq3efxe"
        results = get_events(classification, city, apikey)

        # Check if either number_of_users or gender is empty
        if not classification or not city:
            messages.error(request, "Please enter both a classification and a city.")
        elif not results.get("_embedded", {}).get("events"):
            messages.info(request, "No events found for the given search criteria.")
        else:
            # Store each user's information in a variable
            events = results.get("_embedded", {}).get("events", [])
            events_list = []

            for event in events:
                name = event["name"]
                image_url = event["images"][0]["url"]
                start_date_time = event["dates"]["start"]["dateTime"]
                venue_name = event["_embedded"]["venues"][0]["name"]
                venue_address = event["_embedded"]["venues"][0]["address"]["line1"]
                venue_city = event["_embedded"]["venues"][0]["city"]["name"]
                venue_state = event["_embedded"]["venues"][0]["state"]["name"]
                ticket_link = event["url"]
                eventStartDate = event["dates"]["start"]["dateTime"]

                date_object = datetime.strptime(eventStartDate, "%Y-%m-%dT%H:%M:%SZ")

                # Format the date object to a more readable format, e.g., "Sat Nov 03 2023"
                eventStartDate = date_object.strftime("%a, %b %d, %Y")
                eventStartTime = event["dates"]["start"]["localTime"]
                if eventStartTime:
                    try:
                        time_obj = datetime.strptime(eventStartTime, "%H:%M:%S")
                        formatted_time = time_obj.strftime("%I:%M %p")
                        eventStartTime = formatted_time
                    except ValueError:
                        eventStartTime = "N/A"
                event_details = {
                    "name": name,
                    "date": start_date_time,
                    "img": image_url,
                    "venue_name": venue_name,
                    "address": venue_address,
                    "city": venue_city,
                    "state": venue_state,
                    "ticket": ticket_link,
                    "date_time": eventStartDate,
                    "time": eventStartTime,
                }

                events_list.append(event_details)

            # Create a context dictionary with the user_list and render the 'index.html' template

            context = {"events": events_list}
            return render(request, "ticketmaster.html", context)

    # all other cases, just render the page without sending/passing any context to the template
    return render(request, "ticketmaster.html")


def get_events(classification, city, apikey):
    try:
        # Construct the URL with parameters
        url = "https://app.ticketmaster.com/discovery/v2/events.json"

        # The query parameters will be appended to the url such as
        # https://randomuser.me/api/?results=5&gender=female&nat=us
        params = {"classificationName": classification, "city": city, "apikey": apikey}

        # Send a GET request to the specified URL with parameters
        response = requests.get(url, params=params)

        # Raise an exception for 4xx and 5xx status codes
        response.raise_for_status()

        # Parse the JSON data from the response
        data = response.json()

        # Return the parsed data

        return data
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network issues, timeouts)
        print(f"Request failed: {e}")

        # Return None to indicate failure
        return None


def add_to_favorites(request):
    if request.method == "POST":
        form = AddToFavoritesForm(request.POST)
        if form.is_valid():
            event_name = form.cleaned_data["event_name"]
            event_loc = form.cleaned_data["event_loc"]
            event_img = form.cleaned_data["event_img"]

            # Check if the event is not already in favorites
            if not FavoriteEvent.objects.filter(name=event_name).exists():
                # Add the event to the database
                favorite_event = FavoriteEvent(
                    name=event_name,
                    location=event_loc,
                    image_url=event_img,
                )
                favorite_event.save()

            # Redirect back to the original page after addition
            return redirect("favorites")

    # Redirect to the events page if the addition was not successful
    return redirect("events")


def remove_from_favorites(request):
    if request.method == "POST":
        form = AddToFavoritesForm(request.POST)
        if form.is_valid():
            event_name = form.cleaned_data["event_name"]

            # Check if the event is in favorites
            favorite_event = FavoriteEvent.objects.filter(name=event_name).first()
            if favorite_event:
                # Remove the event from the database
                favorite_event.delete()

            # Redirect back to the favorites page after removal
            return redirect("favorites")

    # Redirect to the events page if the removal was not successful
    return redirect("events")


def favorites(request):
    favorited_events = FavoriteEvent.objects.all()
    context = {"favorited_events": favorited_events}
    return render(request, "favorites.html", context)
