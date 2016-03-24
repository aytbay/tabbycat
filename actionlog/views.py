from django.template import Template, Context
import json

from .models import ActionLogEntry
from utils.views import *
import datetime

@login_required
@tournament_view
def latest_actions(request, t):
    action_objects = []
    actions = ActionLogEntry.objects.filter(tournament=t).order_by(
        '-timestamp')[:15].select_related('user', 'debate', 'ballot_submission')

    timestamp_template = Template("{% load humanize %}{{ t|naturaltime }}")
    for a in actions:
        action_objects.append({
            'user': a.user.username if a.user else a.ip_address or "anonymous",
            'type': a.get_type_display(),
            'param': a.get_parameters_display(),
            'timestamp': timestamp_template.render(Context({'t': a.timestamp})),
        })

    return HttpResponse(json.dumps(action_objects), content_type="text/json")
