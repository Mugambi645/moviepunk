from os import popen
from flask import render_template,request,redirect,url_for,abort
from . import main
from ..requests import getMovies, get_movie,search_movie
from flask_login import login_required
from .. import db,photos

from ..models import User,PhotoProfile
from ..forms import ReviewForm,UpdateProfile
from app import review
from ..forms import ReviewForm
Review = review.Review

#app
@main.route("/")
def index():
    """
    view root page that returns the index page and its data
    """
    message = ""
    #movies
    popular_movies = getMovies("popular")
    upcoming_movie = getMovies("upcoming")
    get_showing_movies = getMovies("now_playing")
    title = "home - Welcome to the best movie review website online"
    search_movie = request.args.get("movie_query")
    if search_movie:
        return redirect(url_for("main.search", movie_name = search_movie))
    else:
        return render_template("index.html", message = message, title = title, popular = popular_movies, upcoming = upcoming_movie, showing = get_showing_movies)

#profile
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)
#movie details
@main.route("/movie/<int:id>")
def movie(id):
    """
    view function that returns movie id and its data
    """
    movie = get_movie(id)
    title = f"{movie.title}"
    review = Review.get_reviews(movie.id)
    return render_template("movie.html", title = title, movie = movie, review = review)


#search movie function
@main.route("/search/<movie_name>")
def search(movie_name):
    """
    View function to display the search results
    """
    movie_name_list = movie_name.split(" ")
    movie_name_format = "+".join(movie_name_list)
    searched_movies = search_movie(movie_name_format)
    title = f" search results for {movie_name}"
    return render_template("search.html", movies=searched_movies)



@main.route('/movie/review/new/<int:id>', methods = ['GET','POST'])
def new_review(id):
    form = ReviewForm()
    movie = get_movie(id)

    if form.validate_on_submit():
        title = form.title.data
        review = form.review.data
        new_review = Review(movie.id,title,movie.poster,review)
    
        new_review.save_review()
       
        return redirect(url_for('main.movie',id = movie.id))

    title = f'{movie.title} review'
    return render_template('new_review.html',title = title, review_form=form, movie=movie)



@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


#photos logic
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))