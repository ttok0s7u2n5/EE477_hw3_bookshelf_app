# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from bookshelf import get_model, oauth2
from flask import Blueprint, redirect, render_template, request, url_for, session


crud = Blueprint('crud', __name__)


# [START list]
@crud.route('/')
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().list(cursor=token)

    return render_template(
        "list.html",
        books=books,
        next_page_token=next_page_token)
# [END list]


# [START list_mine]
@crud.route('/list_mine')
@oauth2.required
def list_mine():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().list_by_user(
        user_id=session['profile']['email'],
        cursor=token)

    return render_template(
        "list.html",
        books=books,
        next_page_token=next_page_token)
# [END list_mine]


# [START list_by_year]
@crud.route('/list_by_year_asc')
@oauth2.required
def list_by_year():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().list_by_year(cursor=token)

    return render_template(
        "list.html",
        books=books,
        next_page_token=next_page_token)
# [END list_by_year]


# [START list_by_year_desc]
@crud.route('/list_by_year_desc')
@oauth2.required
def list_by_year_desc():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().list_by_year_desc(cursor=token)

    return render_template(
        "list.html",
        books=books,
        next_page_token=next_page_token)
# [END list_by_year_desc]


# [START list_by_rate]
@crud.route('/list_by_rate_asc')
@oauth2.required
def list_by_rate():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().list_by_rate(cursor=token)

    return render_template(
        "list.html",
        books=books,
        next_page_token=next_page_token)
# [END list_by_rate]


# [START list_by_rate_desc]
@crud.route('/list_by_rate_desc')
@oauth2.required
def list_by_rate_desc():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().list_by_rate_desc(cursor=token)

    return render_template(
        "list.html",
        books=books,
        next_page_token=next_page_token)
# [END list_by_rate_desc]


# [START insert_title]
@crud.route('/search_by_title', methods=['GET', 'POST'])
def insert_title():
    if request.method == 'POST':
        data = request.form.get('tit')
        return search_by_title(data)
    return render_template("insertTitle.html")
# [END insert_title]


# [START insert_author]
@crud.route('/search_by_author', methods=['GET', 'POST'])
def insert_author():
    if request.method == 'POST':
        data = request.form.get('aut')
        return search_by_author(data)
    return render_template("insertAuthor.html")
# [END insert_author]



# [START search_by_title]
def search_by_title(searchTitle):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    
    #word = request.form['tit']
    books, next_page_token = get_model().search_title(
        tit=searchTitle,
        cursor=token)

    return render_template(
        "list_result.html",
        books=books,
        next_page_token=next_page_token)
# [END search_by_title]


# [START search_by_author]
def search_by_author(searchAuthor):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    #word = request.form['aut']
    books, next_page_token = get_model().search_author(
        aut=searchAuthor,
        cursor=token)

    return render_template(
        "list_result.html",
        books=books,
        next_page_token=next_page_token)
# [END search_by_author]


# [START view]
@crud.route('/<id>')
def view(id):
    book = get_model().read(id)
    return render_template("view.html", book=book)
# [END view]


# [START add]
@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # If the user is logged in, associate their profile with the new book.
        if 'profile' in session:
            data['createdBy'] = session['profile']['name']
            data['createdById'] = session['profile']['email']

        book = get_model().create(data)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Add", book={})
# [END add]


# [START edit]
@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    book = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        book = get_model().update(data, id)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Edit", book=book)
# [END edit]


# [START delete]
@crud.route('/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))
# [END delete]
