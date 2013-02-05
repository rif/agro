# -*- coding: utf-8 -*-

def index():
    resumes = db(active_resumes).select()
    job_offers = db(active_job_offers).select()
    return locals()    


def status():
    s = db(Status.uuid==a0).select().first() if a0 else None
    m = T('Thank you! Your status was recorded.')
    if s:        
        form = crud.update(Status, s.id, next=URL("index"), deletable=False, message=m)
    else:        
        form = crud.create(Status, next=URL("index"), onaccept=new_status, message=m)
    info = T('Information entered here is confidential. It will NOT be displayed publicly.')
    response.view = 'default/form.html'
    return locals()

def resume():
    r = db(Resume.uuid==a0).select().first() if a0 else None
    m = T('Thank you! Your resume was recorded and is pendng approval.')
    if r:
        r.update_record(approved=False)
        form = crud.update(Resume, r.id, next=URL("index"), onaccept=new_resume, deletable=False, message=m)
    else:        
        form = crud.create(Resume, next=URL("index"), onaccept=new_resume, message=m)
    info = T('Part of the information entered here will be made publicly available. We will not display your contact information.')
    response.view = 'default/form.html'
    return locals()

def view_resume():
    resume = Resume(a0) or redirect(URL('index'))
    return locals()

def contact_resume():
    resume = Resume(a0) or redirect(URL('index'))
    form = SQLFORM.factory(
        Field('email', requires=[IS_NOT_EMPTY(), IS_EMAIL()]),
        Field('subject'),
        Field('message', 'text'))
    if form.process().accepted:
        if not form.vars.message.strip():
            session.flash = T('Sorry, no message to send!')
        else:
            mid = Message.insert(email=form.vars.email, to=resume.email, subject=form.vars.subject, content=form.vars.message)
            m = Message(mid)
            mail.send(form.vars.email, T('Confirm your email address!'), 'An message was sent on usambv apps using your email address.\n\
            To confirm your email addres click on the link below:\n%s\n\
            If you did not sent this message, please ignore this email!' % URL('default', 'validate_message', args=m.uuid))
            session.flash = T('An email was send to your address for identity confirmation!')
    elif form.errors:
        session.flash = T('form has errors')
    return locals()

def job_offer():
    j = db(JobOffer.uuid==a0).select().first() if a0 else None
    m = T('Thank you! Your job offer was recorded and is pendng approval.')
    if j:
        j.update_record(approved=False)
        form = crud.update(JobOffer, j.id, next=URL("index"), onaccept=new_job_offer, deletable=False, message=m)
    else:        
        form = crud.create(JobOffer, next=URL("index"), onaccept=new_job_offer, message=m)
    info = T('Part of the information entered here will be made publicly available.')
    response.view = 'default/form.html'
    return locals()

def view_job():
    job = JobOffer(a0) or redirect(URL('index'))
    return locals()

def contact_job():
    job = JobOffer(a0) or redirect(URL('index'))
    form = SQLFORM.factory(
        Field('email', requires=[IS_NOT_EMPTY(), IS_EMAIL()]),
        Field('subject'),
        Field('message', 'text'))
    if form.process().accepted:
        if not form.vars.message.strip():
            session.flash = T('Sorry, no message to send!')
        else:
            mid = Message.insert(email=form.vars.email, to=job.email, subject=form.vars.subject, content=form.vars.message)
            m = Message(mid)
            mail.send(form.vars.email, T('Confirm your email address!'), 'An message was sent on usambv apps using your email address.\n\
            To confirm your email addres click on the link below:\n%s\n\
            If you did not sent this message, please ignore this email!' % URL('default', 'validate_message', args=m.uuid))
            session.flash = T('An email was send to your address for identity confirmation!')
    elif form.errors:
        session.flash = T('form has errors')
    return locals()

def validate_message():
    m = db(Message.uuid==a0).select().first() if a0 else None
    if not m:
        response.flash(T("invalid message!"))
        redirect(URL('index'))
    else:
        m.update_record(approved=True)
        if mail.send(m.to, m.subject, m.content, reply_to=m.email):
            response.flash = T('Thank you, e-mail sent!')
        else:
            response.flash = T('E-mail sending failed. Please contact the site administration!')
    return dict()

def recover():
    form = SQLFORM.factory(Field('email', requires=IS_EMAIL()))
    if form.process().accepted:
        message = 'Link-urile dumneavoastra:\n\n'
        s = db(Status.email == form.vars.email).select().first()
        if s:
            message += 'Status\n'
            message += 'http://%s%s\n' %(request.env.http_host, URL('default', 'status', args=s.uuid))
        r = db(Resume.email == form.vars.email).select().first()
        if r:
            message += 'CV\n'
            message += 'http://%s%s\n' %(request.env.http_host, URL('default', 'resume', args=r.uuid))
        js = db(JobOffer.email == form.vars.email).select()
        if js:
            message += 'Oferte de lucru\n'
            for j in js:
                message += 'http://%s%s\n' %(request.env.http_host, URL('default', 'job_offer', args=j.uuid))

        if mail.send(form.vars.email, "Link-uri de editare", message):
            response.flash = T('Thank you, e-mail sent!')
        else:
            response.flash = T('E-mail sending failed. Please contact the site administration!')
    elif form.errors:
        response.flash = T('form has errors')
    return locals()

def user():
    return dict(form=auth())


def download():
    return response.download(request, db)
