from django.conf.urls import include, url
from interviewer_app.views import dashboard, add_candidate, rate_candidate, get_results

urlpatterns = [
     url(r'^dashboard/$', dashboard, name='dashboard'),
     url(r'^add_candidate/$', add_candidate, name='add_candidate'),
     url(r'^rate_candidate/(?P<candidate_id>(\d+))/$', rate_candidate, name='rate_candidate'),
     url(r'^get_results/$', get_results, name='get_results'),
]
