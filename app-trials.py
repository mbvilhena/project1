
#        username = request.form.get("username")
#        password = request.form.get("password")

#        if not username in users:
#            flash("username not found")
#            return redirect(url_for("login"))
#        else:
#            user = users.username
#        if not password == user["password"]:
#            flash("Incorrect password")
#            return redirect(url_for("login"))
#        else:
#            session["username"] = ["username"]
#            flash("Welcome {{username}}")
#            return redirect(url_for("login"))
#    return render_template("login.html")


#        if request.form["username"] in session ["username"] and request.form["password"] in session["password"]:
#            username = session["username"]
#            flash("Welcome {username}")
#            return render_template("dashboard.html", username=username)
#        flash("Incorrect password")
#    return redirect ("/")
#return render_template("login.html")
