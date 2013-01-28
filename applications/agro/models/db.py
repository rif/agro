# -*- coding: utf-8 -*-

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'gae'
mail.settings.sender = 'usamvb.tm@gmail.com'
#mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

if request.uri_language: T.force(request.uri_language)

import uuid

tracking = db.Table(db, 'tracking',                    
    Field('approved', 'boolean', default=False, writable=False, readable=False, label=T('Approved')),
    Field('enabled', 'boolean', default=True, label=T('Enabled'), comment=T('if you later decide to disable the entry')), 
    Field('uuid', default=lambda:str(uuid.uuid4()), writable=False, readable=False, label=T('UUID')),
    Field('created_on', 'datetime', default=request.now, writable=False, readable=False, label=T('Created on')),
    Field('updated_on', 'datetime', update=request.now, writable=False, readable=False, label=T('Updated on')),
)

Status = db.define_table('status',
    Field('first_name', label=T('First name')),
    Field('last_name', label=T('Last name')),                         
    Field('phone', label=T('Phone')),
    Field('address', label=T('Address')),
    Field('work_place', label=T('Work place')),
    Field('field_of_activity', label=T('Field of activity')),
    Field('work_address', label=T('Work address')),
    Field('work_position', label=T('Work position')),
    Field('email', required=True, requires=[IS_EMAIL(), IS_NOT_IN_DB(db, 'status.email')], unique=True, readable=False, label=T('Email')),
    tracking
)

Resume = db.define_table('resume',
    Field('photo', 'upload', uploadfield='photo_file', label=T('Photo')),
    Field('photo_file', 'blob', label=T('Photo file')),
    Field('first_name', label=T('First name')),
    Field('last_name', label=T('Last name')),
    Field('city', label=T('City')),
    Field('address', label=T('Address')),
    Field('phone', label=T('Phone')),
    Field('completed_studies', label=T('Completed studies')),
    Field('competence_areas', 'list:string', label=T('Competence areas')),
    Field('foreign_languages', 'list:string', label=T('Foreign languages')),
    Field('email', required=True, requires=[IS_EMAIL(), IS_NOT_IN_DB(db, 'resume.email')], unique=True, readable=False, label=T('Email')),
    tracking

)

JobOffer = db.define_table('job_offer',
    Field('company_name', label=T('Company name')),
    Field('city', label=T('City')),
    Field('address', label=T('Address')),
    Field('position_description', 'text', label=T('Position description')),
    Field('available_positions', 'integer', label=T('Available positions')),
    Field('offer_expire_date', 'date', label=T('Offer expire date')),
    Field('email', required=True, requires=IS_EMAIL(), readable=False, label=T('Email')),
    tracking
)

Counter = db.define_table('counter',    
    Field('resume_contact', 'integer', default=0),
    Field('job_contact', 'integer', default=0),
)

#if db(Counter).count() == 0: Counter.insert()

a0, a1 = request.args(0), request.args(1)
active_resumes = ((Resume.approved == True) & (Resume.enabled == True))
active_job_offers = ((JobOffer.approved == True) & (JobOffer.enabled == True) & (JobOffer.offer_expire_date > request.now))

def new_status(form):
    s = Status(form.vars.id) 
    mail.send(form.vars.email,
              "USAMVBT",
              "Puteti edita statusul domneavoastra accesand http://%s%s.\n Cu respect,\nUSAMB" % (request.env.http_host, URL('default', 'status', args=s.uuid)))
    mail.send(to=[a['email'] for a in db(db.auth_user.registration_key == '').select().as_list()],
              subject="USABMV Apps: Status nou",
              message="Pentru a vizualiza accesati: http://%s%s" % (request.env.http_host, URL('backend','backend')))

def new_resume(form):
    r = Resume(form.vars.id)
    mail.send(form.vars.email,
              "USAMVBT",
              "Puteti edita CV-ul domneavoastra accesand http://%s%s.\n Cu respect,\nUSAMB" % (request.env.http_host, URL('default', 'resume', args=r.uuid)))
    mail.send(to=[a['email'] for a in db(db.auth_user.registration_key == '').select().as_list()],
              subject="USABMV Apps: CV nou pentru aprobat",
              message="Accesati CV-ul aici: http://%s%s" % (request.env.http_host, URL('backend','backend')))


def new_job_offer(form):
    j = JobOffer(form.vars.id)
    mail.send(form.vars.email,
              "USAMVBT",
              "Puteti edita oferta domneavoastra accesand http://%s%s.\n Cu respect,\nUSAMB" % (request.env.http_host, URL('default', 'job_offer', args=j.uuid)))
    mail.send(to=[a['email'] for a in db(db.auth_user.registration_key == '').select().as_list()],
              subject="USABMV Apps: Oferta de lucru noua pentru aprobat",
              message="Accesati oferta aici: http://%s%s" % (request.env.http_host, URL('backend','backend')))
