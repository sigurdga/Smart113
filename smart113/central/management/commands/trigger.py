from django.core.management.base import BaseCommand, CommandError
import socket
import json

from smart113.core.models import Phone
from smart113.central.models import Search

class Command(BaseCommand):
    help = 'Trigger search for phone number'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Needs exaclty one argument")
        phone_number = args[0]

        search = Search()
        search.query = phone_number
        search.save()

        results = []
        try:
            number = Phone.objects.get(number=phone_number)
            match = True
            for result in number.userprofile_set.all():
                results.append({'name': result.user.name, 'id': result.id, 'city': result.city})
        except:
            match = False

        address = "localhost"
        port = 7777 # port number is a number, not string

        data = {}
        data['match'] = match
        data['number'] = phone_number
        data['results'] = results
        print json.dumps(data)

        client = socket.socket()
        client.connect((address, port))
        client.send(json.dumps(data))
        print "Done"
        client.close()
