from django.shortcuts import render, redirect
from django.contrib import messages
from django_pandas.io import read_frame
from datetime import datetime, date
import json

from .models import TimeEntry
from .forms import CreateTimeEntryForm


def add_columns_to_dataframe(df):
    # dataframe calculations
    df['start_sec'] = df['time_start'].apply(lambda x: (x.hour * 3600) + (x.minute * 60) + x.second)
    df['end_sec'] = df['time_end'].apply(lambda x: (x.hour * 3600) + (x.minute * 60) + x.second)
    df['rest_sec'] = df['time_rest'].apply(lambda x: (x.hour * 3600) + (x.minute * 60) + x.second)
    df['diff_sec'] = df['end_sec'] - df['start_sec'] - df['rest_sec']

    df['hours_worked'] = df['diff_sec'] // 3600
    df['minutes_worked'] = (df['diff_sec'] - (df['hours_worked'] * 3600)) // 60

    df['str_date'] = df['date'].apply(lambda x: x.strftime('%d.%m.%Y'))
    df['str_hours'] = df['hours_worked'].apply(lambda x: f"0{x}" if x < 10 else f"{x}")
    df['str_minutes'] = df['minutes_worked'].apply(lambda x: f"0{x}" if x < 10 else f"{x}")

    # drop columns from dataframe
    lst_drops = ['start_sec', 'end_sec', 'rest_sec']
    df.drop(lst_drops, axis=1, inplace=True)

    return df


def main(request):
    # database query
    qs = TimeEntry.objects.filter(status_confirmed=False)

    # Create
    form = CreateTimeEntryForm()
    if request.method == 'POST':
        form = CreateTimeEntryForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user_created = str(request.user)
            form.instance.date = request.POST.get('te_date', None)
            form.instance.time_start = request.POST.get('te_time_from', None)
            form.instance.time_end = request.POST.get('te_time_to', None)
            form.instance.time_rest = request.POST.get('te_time_rest', None)
            form.save()
            return redirect("Main")
        else:
            messages.add_message(request, messages.ERROR, "Fehler: Erstellung Zeiteintrag!")
            pass

    context = {'formset': form, 'qs': qs}
    return render(request, 'app_time_calc/main.html', context)


def confirm(request):
    # database query
    qs_open = TimeEntry.objects.filter(status_confirmed=False)
    qs_confirmed = TimeEntry.objects.filter(status_confirmed=True)

    # convert into dataframe
    df_open = read_frame(qs_open)
    df_confirmed = read_frame(qs_confirmed)

    df_open = add_columns_to_dataframe(df_open)
    df_confirmed = add_columns_to_dataframe(df_confirmed)

    # convert into json
    r_open = df_open.to_json(orient='records')
    r_confirmed = df_confirmed.to_json(orient='records')
    r_open_json = json.loads(r_open)
    r_confirmed_json = json.loads(r_confirmed)

    if request.method == 'POST':
        if 'confirm_button' in request.POST:
            TimeEntry.objects.filter(status_confirmed=False).update(status_confirmed=True)
            return redirect("Confirm")
        else:
            pass

    context = {'r_open_json': r_open_json, 'r_confirmed_json': r_confirmed_json}
    return render(request, 'app_time_calc/confirm.html', context)
