@auth.requires_membership('admins')
def backend():
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
