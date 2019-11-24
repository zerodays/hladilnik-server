import json

from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from base.models import Person


def data_to_response(data, status: int = 200) -> HttpResponse:
    """
    Converts data to HttpResponse object with json content type.
    :param data: Data to put into response.
    :param status: Status code of the response.
    :return: HttpResponse object with set json data, content type and status code.
    """
    return HttpResponse(json.dumps(data), content_type='application/json', status=status)


def users_view(request: HttpRequest) -> HttpResponse:
    """
    Displays users (persons) and their balance. Users are sorted by balance and name.
    """
    persons_query = Person.objects.all().order_by('balance', 'name')
    persons = []
    for p in persons_query:
        persons.append({
            'id': p.pk,
            'name': p.name,
            'balance': p.balance,
        })

    return data_to_response(persons)


@csrf_exempt
def add_balance_view(request: HttpRequest) -> HttpResponse:
    """
    Adds balance to specified user (person). Data should be sent as utf-8 encoded json.
    """
    body = request.body.decode('utf-8')
    data = json.loads(body)

    person_id = data.get('id', None)
    balance = data.get('balance', None)

    if person_id is None or balance is None:
        return data_to_response({'error': 'invalid_json'}, status=400)

    person = get_object_or_404(Person, pk=person_id)

    try:
        balance = float(balance)
    except ValueError:
        return data_to_response({'error': 'balance_not_number'}, status=400)

    person.balance += balance
    person.save()

    persons = list(Person.objects.all())
    min_balance = min(map(lambda x: x.balance, persons))

    for p in persons:
        p.balance -= min_balance
        p.save()

    return users_view(request)
