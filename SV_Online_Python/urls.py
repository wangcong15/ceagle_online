from django.conf.urls import url
import view
import asser_rec
import settings
from django.conf.urls.static import static
from django.template import RequestContext

urlpatterns = [
    url(r'^index/', view.index),
    url(r'^filecontent/', view.filecontent),
    url(r'^verify/', view.shell),
    url(r'^login/', view.login),
    url(r'^download/', view.download),
    url(r'^register/', view.register),
    url(r'^update_file/', view.update_file),
    url(r'^asser_rec/', asser_rec.rec_index),
    url(r'^asser_count/', asser_rec.rec_count),
    url(r'^asser_commit/', asser_rec.rec_commit),
    url(r'^asser_add/', asser_rec.rec_addData),
    url(r'^asser_add_api/', asser_rec.rec_addData_api),
    
    url(r'^api/rename_file/', view.rename_file),
    url(r'^api/delete_file/', view.delete_file),
    url(r'^api/create_folder/', view.create_folder),
    url(r'^api/create_file/', view.create_file),
    url(r'^api/assertion_recommendation/', view.assertion_recommendation),
    url(r'^api/accept_common/', view.accept_common),
    url(r'^api/reject_common/', view.reject_common),
    url(r'', view.to_login),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)