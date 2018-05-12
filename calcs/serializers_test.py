from datetime import datetime
from django.utils import timezone
from django.utils.six import BytesIO
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from calcs.models import Measure

from calcs.models import Measure
from calcs.models import Client
from calcs.models import ClientMeasure

from calcs.serializers import MeasureSerializer
from calcs.serializers import ClientSerializer
from calcs.serializers import ClientMeasureSerializer
from calcs.serializers import UserMeasureSerializer
from calcs.serializers import UserSerializer

from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

factory = APIRequestFactory()
request = factory.get('/')


serializer_context = {
    'request': Request(request),
}

# exec(open('serializers_test.py').read())

Client.objects.all().delete()
Measure.objects.all().delete()
ClientMeasure.objects.all().delete()
print(ClientMeasure.objects.all())


gamedatetime = timezone.make_aware(datetime.now(), timezone.get_current_timezone())

cl = Client(created = gamedatetime, name= 'John Smith')
cl.save()

meas = Measure(date = gamedatetime, name='Grishagin', bottom_border = 0.1, upper_border  = 2.0, r = 3.4, epsilon = 0.001)
meas.save()

cl_meas = ClientMeasure(client=cl, measure=meas)
cl_meas.save()

print(meas.pk)
print(meas.name)
print(meas.function_minimum)

print(cl_meas.measure.pk)
print(cl_meas.measure.name)
print(cl_meas.measure.function_minimum)

measure_serializer = MeasureSerializer(instance=meas, context=serializer_context)
print(measure_serializer.data)

client_measure_serializer = ClientMeasureSerializer(instance=cl_meas, context=serializer_context)
print(client_measure_serializer.data)


renderer = JSONRenderer()
rendered = renderer.render(client_measure_serializer.data)
print(rendered)

print(ClientMeasure.objects.all())

cl_meas.delete()
meas.delete()
cl.delete()

'''
json_string_for_new_game = '{"name":"Tomb Raider Extreme Edition","release_date":"2016-05-18T03:02:00.776594Z","game_category":"3D RPG","played":false}'
json_bytes_for_new_game = bytes(json_string_for_new_game json_game_string  , encoding="UTF-8")
stream_for_new_game = BytesIO(json_bytes_for_new_game)
parser = JSONParser()
parsed_new_game = parser.parse(stream_for_new_game)
print(parsed_new_game)

new_game_serializer = GameSerializer(data=parsed_new_game)
if new_game_serializer.is_valid():
    new_game = new_game_serializer.save()
    print(new_game.name)'''