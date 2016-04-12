
from django.contrib import admin
from interviewer_app.models import Candidate, Score

class CandidateAdmin(admin.ModelAdmin):
 list_display = ( 'first_name', 'last_name', 'email' )
 search_fields = [ 'first_name' ]
 
 
class ScoreAdmin(admin.ModelAdmin):
 list_display = ( 'interviwer',  'candidate', 'score' )
 

admin.site.register(Candidate,CandidateAdmin)
admin.site.register(Score,ScoreAdmin)