from flask import request, redirect, url_for, session, render_template
from datetime import date

@app.route('/update_guest/<reg_id>', methods=['GET', 'POST'])
def update_guest(reg_id):
    # Only allow update if the record is from today
    registration = supabase.table("guest_registrations").select("*").eq("id", reg_id).single().execute().data
    if registration and registration["visit_date"] == str(date.today()):
        if request.method == "POST":
            # get updated info from form, e.g. request.form["guest_name"]
            supabase.table("guest_registrations").update({
                "guest_name": request.form["guest_name"],
                "company": request.form["company"],
                "visiting_person": request.form["visiting_person"],
                "guest_id_number": request.form["guest_id_number"],
                # handle file/photo update if needed
            }).eq("id", reg_id).execute()
            return redirect(url_for('dashboard'))
        # GET: Show update form pre-filled with current info
        return render_template("update_guest.html", reg=registration)
    return "Update not allowed (Can only edit today's registrations)", 403