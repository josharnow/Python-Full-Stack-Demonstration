from flask import render_template, redirect, session, request, flash
from flask_app import app

from flask_app.models.user import User
from flask_app.models.company import Company

@app.route('/companies')
def company_index():
  if 'user_id' not in session:
    flash('Please log in to view this page.')
    return redirect('/')
  
  else:
    data = {
      'user_id': session['user_id']
    }
    # companies = Company.get_all_companies(data)
    companies = Company.get_all_companies()
    # companies = Company.get_all_companies_from_user(data)
    print(companies)
    return render_template('companies.html', companies = companies)

@app.route('/companies/new')
def new_company():
  return render_template('new_company.html')

@app.route('/companies/create', methods=['POST'])
def add_company():
  if Company.validate_company(request.form):
    # Create company here
    data = {
      'name': request.form['name'],
      'ticker_symbol': request.form['ticker_symbol'],
      'stock_exchange': request.form['stock_exchange'],
      'shares_owned': request.form['shares_owned'],
      'cost_basis': request.form['cost_basis'],
      'user_id': session['user_id'] # user_id is stored in session by login_user() in login.py
    }
    
    Company.add_company(data)
    
    print('Company is valid')
    return redirect('/companies')
  
  else:
    print('Company is invalid')
    return redirect('/companies/new')
  
@app.route('/companies/<int:company_id>')
def company_info(company_id):
  company = Company.get_company_by_id({'id': company_id})
      
  if session['user_id'] != company.user.id:
    flash(f'Please log in as the appropriate user to view this page (Company ID #{company.id}).')
    return redirect('/companies')
  
  else:
    return render_template('company_info.html', company = company)
  
@app.route('/companies/<int:company_id>/edit')
def edit_company(company_id):
  company = Company.get_company_by_id({'id': company_id})
  
  if session['user_id'] != company.user.id:
    flash(f'Please log in as the appropriate user to view this page (Company ID #{company.id}).')
    return redirect('/companies')

  else:
    return render_template('edit_company.html', company = company)

@app.route('/companies/<int:company_id>/add_or_remove')
def add_or_remove_assets(company_id):
  company = Company.get_company_by_id({'id': company_id})
  
  if session['user_id'] != company.user.id:
    flash(f'Please log in as the appropriate user to view this page (Company ID #{company.id}).')
    return redirect('/companies')

  else:
    return render_template('add_or_remove_assets.html', company = company)

@app.route('/companies/<int:company_id>/update', methods=['POST'])
def update_company(company_id):
  company = Company.get_company_by_id({'id': company_id})
  
  if session['user_id'] != company.user.id:
    flash(f'Please log in as the appropriate user to view this page (Company ID #{company.id}).')
    return redirect('/companies')
  
  else:
    if Company.validate_company(request.form):
      data = {
        'name': request.form['name'],
        'ticker_symbol': request.form['ticker_symbol'],
        'stock_exchange': request.form['stock_exchange'],
        'shares_owned': request.form['shares_owned'],
        'cost_basis': request.form['cost_basis'],
        'id': company_id
      }
      Company.update_company(data)
      return redirect(f'/companies/{company_id}')
    
    else:
      return redirect(f'/companies/{company_id}/edit')
    
@app.route('/companies/<int:company_id>/delete')
def delete_company(company_id):
  company = Company.get_company_by_id({'id': company_id})
  
  if session['user_id'] != company.user.id:
    flash(
        f'Please log in as the appropriate user to view this page (Company ID #{company.id}).')
    return redirect('/companies')
  
  else:
    return render_template('delete_company.html', company = company)

@app.route('/companies/<int:company_id>/confirm')
def confirm_delete_company(company_id):
  company = Company.get_company_by_id({'id': company_id})
  company.delete_company({'id': company_id})
  
  return redirect('/companies')
