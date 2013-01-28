@auth.requires_membership('admins')
def backend():
    statuses = db(Status.approved==False).select()
    resumes = db(Resume.approved==False).select()
    job_offers = db(JobOffer.approved==False).select()
    return locals()

@auth.requires_membership('admins')
def statuses():
    grid = SQLFORM.grid(Status)
    response.title = T('Statuses')
    response.view = 'backend/grid.html'
    return locals()

@auth.requires_membership('admins')
def resumes():
    grid = SQLFORM.grid(Resume)
    response.title = T('Resumes')
    response.view = 'backend/grid.html'
    return locals()

@auth.requires_membership('admins')
def job_offers():
    grid = SQLFORM.grid(JobOffer)
    response.title = T('Job Offers')
    response.view = 'backend/grid.html'
    return locals()

@auth.requires_membership('admins')
def approve_resume():
    r = Resume(a0)
    if r: r.update_record(approved=True)
    return T('Resume approved!')

@auth.requires_membership('admins')
def delete_resume():
    del Resume[a0]
    return T('Resume deleted!')

@auth.requires_membership('admins')
def approve_job_offer():
    j = JobOffer(a0)
    if j: j.update_record(approved=True)
    return T('Job offer approved!')

@auth.requires_membership('admins')
def delete_job_offer():
    del JobOffer[a0]
    return T('Job offer deleted!')
