from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _
from django.views.generic.create_update import create_object, update_object

from generic_views.views import generic_assign_remove, \
                                generic_delete, \
                                generic_detail, generic_list

from photos.views import generic_photos

from inventory import location_filter

from assets import person_record_links, asset_record_links, state_record_links, group_record_links
from models import Item, ItemGroup, Person, State
from forms import ItemForm, ItemForm_view, ItemGroupForm, PersonForm, PersonForm_view
from conf import settings as asset_settings                             

                                
urlpatterns = patterns('assets.views',
    url(r'^person/(?P<object_id>\d+)/photos/$', generic_photos, {'model':Person, 'max_photos':asset_settings.MAX_PERSON_PHOTOS}, 'person_photos'), 
    url(r'^person/(?P<object_id>\d+)/$', generic_detail, {'form_class':PersonForm_view, 'queryset':Person.objects.all(), 'create_view':'person_create', 'record_links':person_record_links, 'extra_context':{'subtemplates':['generic_photos_subtemplate.html']}}, 'person_view'),
    url(r'^person/list/$', generic_list, {'queryset':Person.objects.all(), 'list_filter':location_filter, 'extra_context':{'title':_(u'people'), 'create_view':"person_create", 'record_links':person_record_links}}, 'person_list'),
    url(r'^person/create/$', create_object, {'form_class':PersonForm, 'template_name':'generic_form.html'}, 'person_create'),
    url(r'^person/(?P<object_id>\d+)/update/$', update_object, {'form_class':PersonForm, 'template_name':'generic_form.html'}, 'person_update'),
    url(r'^person/(?P<object_id>\d+)/delete/$', generic_delete, {'model':Person, 'post_delete_redirect':'person_list', 'extra_context':{'title':_(u'person')}}, 'person_delete'),
    url(r'^person/(?P<object_id>\d+)/assign/$', 'person_assign_remove_item', (), 'person_assign_item'),

    url(r'^asset/create/$', create_object, {'form_class':ItemForm, 'template_name':'generic_form.html'}, 'item_create'),
    url(r'^asset/(?P<object_id>\d+)/update/$', update_object, {'form_class':ItemForm, 'template_name':'generic_form.html'}, 'item_update'),
    url(r'^asset/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':Item}, post_delete_redirect="item_list", extra_context=dict(title=_(u'asset'))), 'item_delete'),
    url(r'^asset/(?P<object_id>\d+)/assign/$', 'item_assign_remove_person', (), name='item_assign_person'),
    url(r'^asset/orphans/$', generic_list, dict({'queryset':Item.objects.filter(person=None)}, list_filter=location_filter, extra_context=dict(title=_(u'orphan assets'), create_view='item_create', record_links=asset_record_links)), 'item_orphans_list'),
    url(r'^asset/list/$', generic_list, dict({'queryset':Item.objects.all()}, list_filter=location_filter, extra_context=dict(title=_(u'assets'), create_view='item_create', record_links=asset_record_links)), 'item_list'),
    url(r'^asset/(?P<object_id>\d+)/$', generic_detail, dict(form_class=ItemForm_view, queryset=Item.objects.all(), create_view='item_create', record_links=asset_record_links, extra_context={'subtemplates':['generic_photos_subtemplate.html', 'state_subtemplate.html']}, extra_fields=[{'field':'get_owners', 'label':_(u'Assigned to:')}]), 'item_view'),
    url(r'^asset/(?P<object_id>\d+)/photos/$', generic_photos, dict(model=Item, max_photos=asset_settings.MAX_ASSET_PHOTOS), 'item_photos'), 
    url(r'^asset/(?P<object_id>\d+)/state/(?P<state_id>\d+)/set/$', 'item_setstate', (), 'item_setstate'),
    url(r'^asset/(?P<object_id>\d+)/state/(?P<state_id>\d+)/unset$', 'item_remove_state', (), 'item_remove_state'),
    url(r'^asset/state/init/$', 'item_state_list_init', (), 'item_state_list_init'),
    url(r'^asset/state/(?P<state_id>\d+)/list/$', 'item_state_list', (), 'item_state_list'),

    url(r'^group/list/$', generic_list, dict({'queryset':ItemGroup.objects.all()}, extra_context=dict(title=_(u'item groups'), create_view='group_create', record_links=group_record_links)), 'group_list'),
    url(r'^group/create/$', create_object, {'form_class':ItemGroupForm, 'template_name':'generic_form.html'}, 'group_create'),
    url(r'^group/(?P<object_id>\d+)/$', generic_detail, dict(form_class=ItemGroupForm, queryset=ItemGroup.objects.all(), create_view='group_create', record_links=group_record_links), 'group_view'),
    url(r'^group/(?P<object_id>\d+)/update/$', 'group_assign_remove_item', (), name='group_update'),
    url(r'^group/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':ItemGroup}, post_delete_redirect="group_list", extra_context=dict(title=_(u'item group'))), 'group_delete'),

    url(r'^state/list/$', generic_list, dict({'queryset':State.objects.all()}, extra_context=dict(title =_(u'states'), create_view='state_create', record_links=state_record_links)), 'state_list'),
    url(r'^state/create/$', create_object, {'model':State, 'template_name':'generic_form.html'}, 'state_create'),
    url(r'^state/(?P<object_id>\d+)/update/$', update_object, {'model':State, 'template_name':'generic_form.html'}, 'state_update'),
    url(r'^state/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':State}, post_delete_redirect="state_list", extra_context=dict(title=_(u'states'))), 'state_delete'),
)
    

