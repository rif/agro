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
mail.settings.sender = 'fericean@gmail.com'
#mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

if request.uri_language: T.force(request.uri_language)

import uuid

tracking = db.Table(db, 'tracking',
                    Field('email', required=True, requires=[IS_EMAIL(), IS_NOT_IN_DB(db, 'status.email')], unique=True, readable=False),
                    Field('approved', 'boolean', default=False, writable=False, readable=False),
                    Field('enabled', 'boolean', default=True, writable=False, readable=False),
                    Field('uuid', default=lambda:str(uuid.uuid4()), writable=False, readable=False),
                    Field('created_on', 'datetime', default=request.now, writable=False, readable=False),
                    Field('updated_on', 'datetime', update=request.now, writable=False, readable=False),
)

db._common_fields.append(tracking)

Status = db.define_table('status',
                         Field('first_name'),
                         Field('last_name'),                         
                         Field('phone'),
                         Field('address', 'text'),
                         Field('work_place'),
                         Field('work_field_of_activity'),
                         Field('work_address', 'text'),
                         Field('work_position'),
)

Resume = db.define_table('resume',
                         Field('photo', 'upload', uploadfield='photo_file'),
                         Field('photo_file', 'blob'),
                         Field('first_name'),
                         Field('last_name'),
                         Field('city'),
                         Field('address', 'text'),
                         Field('phone'),
                         Field('completed_studies'),
                         Field('competence_areas', 'list:string'),
                         Field('foreign_languages', 'list:string'),

)

JobOffer = db.define_table('job_offer',
                            Field('company_name'),
                            Field('city'),
                            Field('address', 'text'),
                            Field('position_description', 'text'),
                            Field('available_positions', 'integer'),
                            Field('offer_expire_date', 'date'),
)

a0, a1 = request.args(0), request.args(1)
active_resumes = ((Resume.approved == True) & (Resume.enabled == True))
active_job_offers = ((JobOffer.approved == True) & (JobOffer.enabled == True) & (JobOffer.offer_expire_date > request.now))
