from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

class Company:
  def __init__(self, data):
    self.id = data['id']
    self.name = data['name']
    self.ticker_symbol = data['ticker_symbol']
    self.stock_exchange = data['stock_exchange']
    self.shares_owned = data['shares_owned']
    self.cost_basis = data['cost_basis']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']
    self.user_id = data['user_id']
    self.user = None
    
  @classmethod
  def add_company(cls, data):
    query = "INSERT INTO companies (name, ticker_symbol, stock_exchange, shares_owned, cost_basis, user_id) VALUES (%(name)s, %(ticker_symbol)s, %(stock_exchange)s, %(shares_owned)s, %(cost_basis)s, %(user_id)s);"

    result = connectToMySQL('user_portfolio').query_db(query, data)

    return result
  
  @classmethod
  def get_all_companies(cls):
  # def get_all_companies(cls, data):
    query = 'SELECT * FROM companies JOIN users ON companies.user_id = users.id;'
    # query = 'SELECT * FROM companies WHERE companies.user_id = 1;'
    # query = 'SELECT * FROM companies WHERE companies.user_id = 1;'
    
    results = connectToMySQL('user_portfolio').query_db(query)
    
    companies = []
    
    for item in results:
      company = cls(item)
      user_data = {
        'id': item['users.id'],
        'username': item['username'],
        'email': item['email'],
        'password': item['password'],
        'created_at': item['users.created_at'],
        'updated_at': item['users.updated_at']
        
      }
      company.user = User(user_data)
      companies.append(company)
    
    return companies
    
  @classmethod
  def get_all_companies_from_user(cls, data): # Data is passed in from company_index() in companies.py
    # query = 'SELECT * FROM companies JOIN users ON companies.user_id = user.id;'
    # query = 'SELECT * FROM companies WHERE companies.user_id = 1;'
    query = 'SELECT * FROM companies WHERE companies.user_id = %(user_id)s;'
    
    results = connectToMySQL('user_portfolio').query_db(query, data)
    
    companies = []

    for item in results:
      company = cls(item)
      user_data = {
          'id': item['users.id'],
          'username': item['username'],
          'email': item['email'],
          'password': item['password'],
          'created_at': item['users.created_at'],
          'updated_at': item['users.updated_at']

      }
      company.user = User(user_data)
      companies.append(company)

    return companies
  
  @classmethod
  def get_company_by_id(cls, data):
    query = "SELECT * FROM companies JOIN users ON companies.user_id = users.id WHERE companies.id = %(id)s;"
    
    result = connectToMySQL('user_portfolio').query_db(query, data)
    
    company = cls(result[0])
    user_data = {
        'id': result[0]['users.id'],
        'username': result[0]['username'],
        'email': result[0]['email'],
        'password': result[0]['password'],
        'created_at': result[0]['users.created_at'],
        'updated_at': result[0]['users.updated_at']

    }
    company.user = User(user_data)
    
    return company
  
  @classmethod
  def update_company(cls, data):
    query = 'UPDATE companies SET name = %(name)s, ticker_symbol = %(ticker_symbol)s, stock_exchange = %(stock_exchange)s , shares_owned = %(shares_owned)s, cost_basis = %(cost_basis)s WHERE id = %(id)s;'
    
    connectToMySQL('user_portfolio').query_db(query, data)
    
  @classmethod
  def delete_company(cls, data):
    query = 'DELETE FROM companies WHERE id = %(id)s;'
    
    connectToMySQL('user_portfolio').query_db(query, data)
  
  @staticmethod
  def validate_company(data):
    is_valid = True

    if len(data['name']) < 1 or len(data['name']) > 100:
      flash("Asset name should be between 1 and 100 characters.")
      is_valid = False
      
    if len(data['ticker_symbol']) > 5:
      flash("Ticker symbol should be less than 6 characters.")
      is_valid = False
      
    if len(data['stock_exchange']) > 45:
      flash("Stock exchange should be less than 46 characters.")
      is_valid = False
    
    if len(data['shares_owned']) == 0 or int(data['shares_owned']) < 1:
      flash("Shares purchased should be greater than 0.")
      is_valid = False
      
    if len(data['cost_basis']) == 0 or len(data['cost_basis']) > 0 and float(data['cost_basis']) < 0:
      flash("Cost should be greater than 0.")
      is_valid = False
      
    return is_valid