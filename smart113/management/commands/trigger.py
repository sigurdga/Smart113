from django.core.management.base import BaseCommand, CommandError
import socket

class Command(BaseCommand):
    help = 'Trigger search for phone number'

    def handle(self, *args, **options):
        if len(args != 1):
            raise CommandError("Needs exaclty one argument")
        phone_number = args[0]

        address = "localhost"
        port = 7777 # port number is a number, not string

        client = socket.socket()
        client.connect((address, port))
        print phone_number
        client.send(phone_number)
        print "Done"
        client.close()
