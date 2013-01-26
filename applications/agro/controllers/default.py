# -*- coding: utf-8 -*-

def index():
    resumes = db(active_resumes).select()
    job_offers = db(active_job_offers).select()
    return locals()

def status():
    form = crud.create(Status, next=URL("index"), message=T('Thank you! Your status was recorded.'))
    response.view = 'default/form.html'
    return locals()

def resume():
    form = crud.create(Resume, next=URL("index"), message=T('Thank you! Your resume was recorded and is pendng approval.'))
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
            if mail.send(resume.email, form.vars.subject, form.vars.message):
                session.flash = T('Thank you, e-mail sent!')
            else:
                session.flash = T('E-mail sending failed. Please contact the site administration!')
    elif form.errors:
        session.flash = T('form has errors')
    return locals()

def job_offer():
    form = crud.create(JobOffer, next=URL("index"), message=T('Thank you! Your job offer was recorded and is pendng approval.'))
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
            else:
                session.flash = T('E-mail sending failed. Please contact the site administration!')
    elif form.errors:
        session.flash = T('form has errors')
    return locals()


def user():
    return dict(form=auth())


def download():
    return response.download(request, db)
