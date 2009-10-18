from django.views.generic.list_detail import object_list
from mysite.proxy.models import Invite, Relation 
from django import forms
from django.http import HttpResponseRedirect
import datetime

class InviteForm(forms.Form):
    email = forms.EmailField()

def invites(request):
    if request.method == 'GET':
        invites = Invite.objects.filter(invited_email__exact=request.user.email)
        form= InviteForm()
        return object_list(request, queryset=invites, extra_context={'form': form})
    elif request.method == 'POST':
        form = InviteForm(request.POST)
        #TODO add logic for only allowing proxy requests from one person to another how often?
        if form.is_valid():
            i = Invite(granter_id=request.user.id,granter_name=request.user.first_name,invited_email=form.cleaned_data['email'],date=datetime.datetime.now())
            i.save()
            return HttpResponseRedirect('/proxy/invite/')


def relations(request,extra=None):
    if request.method == 'GET':
        relations = Relation.objects.filter(acceptor_id=str(request.user.id))
        granted_list = Relation.objects.filter(granter_id=str(request.user.id))
        return object_list(request, queryset=relations, extra_context={'granted_list': granted_list})
    elif request.method == 'POST':
        _meth = request.POST.get('method', 'post')
        if _meth == 'post':
            #TODO only allow claiming proxy once per person to person relationship
            _id = request.POST['invite_id']
            g_i = Invite.objects.filter(id__exact=_id)
            r = Relation(invitation_id=g_i[0],acceptor_id=request.user.id,acceptor_name=request.user.first_name,\
            granter_id=g_i[0].granter_id,granter_name=g_i[0].granter_name,date=datetime.datetime.now())
            r.save()
            return HttpResponseRedirect('/proxy')
	if _meth == 'delete':
		_id = request.POST['relation_id']
        relations = Relation.objects.filter(id=_id)
        relations[0].delete()
        return HttpResponseRedirect('/proxy')
