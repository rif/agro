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
    response.view = 'default/form.html'
    return locals()

def resume():
    r = db(Resume.uuid==a0).select().first() if a0 else None
    m = T('Thank you! Your resume was recorded and is pendng approval.')
    if r:
        form = crud.update(Resume, r.id, next=URL("index"), deletable=False, message=m)
    else:        
        form = crud.create(Resume, next=URL("index"), onaccept=new_resume, message=m)
    response.view = 'default/form.html'
    return locals()

def view_resume():
    resume = Resume(a0) or redirect(URL('index'))
    return locals()

def contact_resume():
    resume = Resume(a0) or redirect(URL('index'))
    form = SQLFORM.factory(
        Field('subject'),
        Field('message', 'text'))
    if form.process().accepted:
        if not form.vars.message.strip():
            session.flash = T('Sorry, no message to send!')
        else:
            if mail.send(resume.email, form.vars.subject or 'USAMVBT', form.vars.message):
                session.flash = T('Thank you, e-mail sent!')
                c = db(Counter).select().first()
                c.update_record(resume_contact = c.resume_contact + 1)
            else:
                session.flash = T('E-mail sending failed. Please contact the site administration!')
    elif form.errors:
        session.flash = T('form has errors')
    return locals()

def job_offer():
    j = db(JobOffer.uuid==a0).select().first() if a0 else None
    m = T('Thank you! Your job offer was recorded and is pendng approval.')
    if j:
        form = crud.update(JobOffer, j.id, next=URL("index"), deletable=False, message=m)
    else:        
        form = crud.create(JobOffer, next=URL("index"), onaccept=new_job_offer, message=m)
    response.view = 'default/form.html'
    return locals()

def view_job():
    job = JobOffer(a0) or redirect(URL('index'))
    return locals()

def contact_job():
    job = JobOffer(a0) or redirect(URL('index'))
    form = SQLFORM.factory(
        Field('subject'),
        Field('message', 'text'))
    if form.process().accepted:
        if not form.vars.message.strip():
            session.flash = T('Sorry, no message to send!')
        else:
            if mail.send(job.email, form.vars.subject, form.vars.message):
                session.flash = T('Thank you, e-mail sent!')
                c = db(Counter).select().first()
                c.update_record(job_contact = c.job_contact + 1)
            else:
                session.flash = T('E-mail sending failed. Please contact the site administration!')
    elif form.errors:
        session.flash = T('form has errors')
    return locals()

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
