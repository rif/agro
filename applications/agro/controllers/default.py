# -*- coding: utf-8 -*-

def index():
    grid = db(Resume).select()
    return locals()

def status():
    session.forget()
    form = crud.create(Status)
    response.view = 'default/form.html'
    return locals()

def resume():
    session.forget()
    form = crud.create(Resume)
    response.view = 'default/form.html'
    return locals()

def work_offer():
    session.forget()
    form = crud.create(WorkOffer)
    response.view = 'default/form.html'
    return locals()

def user():
    return dict(form=auth())


def download():
    return response.download(request, db)
