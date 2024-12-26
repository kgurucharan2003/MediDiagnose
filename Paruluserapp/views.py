from django.shortcuts import render, redirect
from django.contrib import messages
from Paruluserapp.models import pusermodel, hdpmodel, kdpmodel, bdpmodel, dpmodel, ldpmodel
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from django.contrib import messages


def puser(request):
    return render(request, "user/puserlogin.html")

def puserregister(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("pswd")
        phone = request.POST.get("phone")
        city = request.POST.get("city")
        print(name, email, password, phone, city)
        form1 = pusermodel(name=name, email=email, pswd=password, phone=phone, city=city)
        form1.save()
        messages.success(request, "Registered successfully")
        return render(request,'user/puserlogin.html')  
    else:
        return render(request, "user/puserregister.html")
    
def puserloginaction(request):
    if request.method == "POST":
        uname = request.POST.get("email")
        pswd = request.POST.get("pswd")
        print(uname, pswd)
        try:
            check = pusermodel.objects.get(email=uname, pswd=pswd)
            request.session['user_email'] = check.email
            return render(request, "user/puserhome.html")
        except:
            messages.error(request, "Invalid username or password")
    return render(request, "user/puserlogin.html")

def puserhome(request):
    return render(request, "user/puserhome.html")

def puserlogout(request):
    return render(request, "user/puserlogin.html")

def contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Construct the email content
        full_message = f"From: {name}\nEmail: {email}\n\nMessage:\n{message}"

        # Send the email
        try:
            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],  # Send to your own email
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again later.')
            
        return redirect('contact')  # Redirect back to the form page
def hdp(request):
    return render(request, "user/hdp.html")

def hdpaction(request):
    if request.method == "POST":
        # Extract data from POST request
        age = request.POST.get("age")
        sex = request.POST.get("sex")
        cp = request.POST.get("cp")
        trestbps = request.POST.get("trestbps")
        chol = request.POST.get("chol")
        fbs = request.POST.get("fbs")
        restecg = request.POST.get("restecg")
        thalach = request.POST.get("thalach")
        exang = request.POST.get("exang")
        oldpeak = request.POST.get("oldpeak")
        slope = request.POST.get("slope")
        ca = request.POST.get("ca")
        thal = request.POST.get("thal")
        
        # Load dataset and prepare the model
        df = pd.read_csv('media/heart.csv')
        X = df.drop('target', axis=1)
        y = df['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        
        # Train the model
        model = SVC(kernel='linear', C=1.0, random_state=42)
        model.fit(X_train, y_train)
        
        custom_data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
        custom_data_scaled = scaler.transform(custom_data)
        custom_predictions = model.predict(custom_data_scaled)
        
        # Retrieve user email
        user_email = request.session.get('user_email')
        
        # Save the prediction result to the database
        hdpmodel(age=age, sex=sex, cp=cp, trestbps=trestbps, chol=chol, fbs=fbs, restecg=restecg, thalach=thalach, exang=exang, oldpeak=oldpeak, slope=slope, ca=ca, thal=thal, user_email=user_email, custom_predictions=custom_predictions).save()

        # Prepare prediction message and result class
        if custom_predictions == 1:
            prediction_message = "Heart Disease Detected"
            result_class = "result-detected"
            disease_type = "Heart Disease"
        else:
            prediction_message = "Heart Disease Not Detected"
            result_class = "result-not-detected"
            disease_type = "Heart Disease"
        
        # Send email only once after prediction is made
        if user_email:
            subject = 'Heart Disease Prediction Result'
            from_email = settings.EMAIL_HOST_USER
            to_email = [user_email]
            
            
            html_content = render_to_string('user/email_template.html', {
                'prediction_message': prediction_message,
                'result_class': result_class,
                'disease_type': disease_type
            })

            msg = EmailMultiAlternatives(subject, '', from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        messages.success(request, prediction_message)
        return render(request, "user/hdp.html")

    else:
        return render(request, "user/hdp.html")


def kdp(request):
    return render(request, "user/kdp.html")

def kdpaction(request):
    if request.method == "POST":
        bp = request.POST.get("Bp")
        sg = request.POST.get("Sg")
        al = request.POST.get("Al")
        su = request.POST.get("Su")
        rbc = request.POST.get("Rbc")
        bu = request.POST.get("Bu")
        sc = request.POST.get("Sc")
        sod = request.POST.get("Sod")
        pot = request.POST.get("Pot")
        hemo = request.POST.get("Hemo")
        wbcc = request.POST.get("Wbcc")
        rbcc = request.POST.get("Rbcc")
        htn = request.POST.get("Htn")
        df = pd.read_csv('media/kidney.csv')
        X = df.drop('Class', axis=1)
        y = df['Class']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        model = SVC(kernel='linear', C=1.0, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        custom_data = np.array([[bp, sg, al, su, rbc, bu, sc, sod, pot, hemo, wbcc, rbcc, htn]])
        custom_data_scaled = scaler.transform(custom_data)
        custom_predictions = model.predict(custom_data_scaled)
        print("Custom predictions:", custom_predictions)
        user_email = request.session.get('user_email')
        if custom_predictions == 1:
            prediction_message = "Kidney Disease Detected"
            result_class = "result-detected"
            disease_type = "Kidney Disease"
        else:
            prediction_message = "Kidney Disease Not Detected"
            result_class = "result-not-detected"
            disease_type = "Kidney Disease"

        kdpmodel(bp=bp, sg=sg, al=al, su=su, rbc=rbc, bu=bu, sc=sc, sod=sod, pot=pot, hemo=hemo, wbcc=wbcc, rbcc=rbcc, htn=htn, user_email=user_email, custom_predictions=custom_predictions).save()

        if user_email:
            subject = 'Kidney Disease Prediction Result'
            from_email = settings.EMAIL_HOST_USER
            to_email = [user_email]

            html_content = render_to_string('user/email_template.html', {
                'prediction_message': prediction_message,
                'result_class': result_class,
                'disease_type': disease_type
            })
            
            msg = EmailMultiAlternatives(subject, '', from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        messages.success(request, prediction_message)
        return render(request, "user/kdp.html")
        
    else:
        return render(request, "user/kdp.html")

def bdp(request):
    return render(request, "user/bdp.html")

def bdpaction(request):
    if request.method=="POST":
        age = request.POST.get("Age")
        menopause = request.POST.get("Menopause")
        Tumor = request.POST.get("Tumor")
        InvNodes = request.POST.get("Inv-Nodes")
        Breast = request.POST.get("Breast")
        Metastasis = request.POST.get("Metastasis")
        BreastQuadrant = request.POST.get("Breast-Quadrant")
        History = request.POST.get("History")
        df = pd.read_csv('media/breast cancer.csv')
        X = df.drop('Diagnosis Result', axis=1)
        y = df['Diagnosis Result']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        model = SVC(kernel='linear', C=1.0, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        custom_data = np.array([[age, menopause, Tumor, InvNodes, Breast, Metastasis, BreastQuadrant, History]])
        custom_data_scaled = scaler.transform(custom_data)
        custom_predictions = model.predict(custom_data_scaled)
        print("Custom predictions:", custom_predictions)
        user_email = request.session.get('user_email')
        if custom_predictions == 1:
            prediction_message = "Breast Cancer Detected"
            result_class = "result-detected"
            disease_type = "Breast Cancer Disease"
        else:
            prediction_message = "Breast Cancer Not Detected"
            result_class = "result-not-detected"
            disease_type = "Breast Cancer Disease"

        # Save the result in the database
        bdpmodel(age=age, menopause=menopause, Tumor=Tumor, InvNodes=InvNodes, Breast=Breast, Metastasis=Metastasis, BreastQuadrant=BreastQuadrant, History=History, user_email=user_email, custom_predictions=custom_predictions).save()

        # Send email to user
        if user_email:
            subject = 'Breast Cancer Prediction Result'
            from_email = settings.EMAIL_HOST_USER
            to_email = [user_email]

            html_content = render_to_string('user/email_template.html', {
                'prediction_message': prediction_message,
                'result_class': result_class,
                'disease_type': disease_type
            })

            msg = EmailMultiAlternatives(subject, '', from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        messages.success(request, prediction_message)
        return render(request, "user/bdp.html")
    else:
        return render(request, "user/bdp.html")
    

def dp(request):
    return render(request, "user/dp.html")

def dpaction(request):
    if request.method == "POST":
        pregnancies = request.POST.get("Pregnancies")
        glucose = request.POST.get("Glucose")
        bloodpressure = request.POST.get("BloodPressure")
        skinthickness = request.POST.get("SkinThickness")
        insulin = request.POST.get("Insulin")
        bmi = request.POST.get("BMI")
        diabetespedigreefunction = request.POST.get("DiabetesPedigreeFunction")
        age = request.POST.get("Age")
        df = pd.read_csv('media/diabetes.csv')
        X = df.drop('Outcome', axis=1)
        y = df['Outcome']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        model = SVC(kernel='linear', C=1.0, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        custom_data = [[pregnancies, glucose, bloodpressure, skinthickness, insulin, bmi, diabetespedigreefunction, age]]
        custom_data_scaled = scaler.transform(custom_data)
        custom_predictions = model.predict(custom_data_scaled)
        print("Custom predictions:", custom_predictions)
        user_email = request.session.get('user_email')
        if custom_predictions == 1:
            prediction_message = "Diabetes Detected"
            result_class = "result-detected"
            disease_type = "Diabetes Disease"
        else:
            prediction_message = "Diabetes Not Detected"
            result_class = "result-not-detected"
            disease_type = "Diabetes Disease"

        # Save the result in the database
        dpmodel(pregnancies=pregnancies, glucose=glucose, bloodpressure=bloodpressure, skinthickness=skinthickness, insulin=insulin, bmi=bmi, diabetespedigreefunction=diabetespedigreefunction, age=age, user_email=user_email, custom_predictions=custom_predictions).save()

        # Send email to user
        if user_email:
            subject = 'Diabetes Prediction Result'
            from_email = settings.EMAIL_HOST_USER
            to_email = [user_email]

            html_content = render_to_string('user/email_template.html', {
                'prediction_message': prediction_message,
                'result_class': result_class,
                'disease_type': disease_type
            })

            msg = EmailMultiAlternatives(subject, '', from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        messages.success(request, prediction_message)
        return render(request, "user/dp.html")
    else:
        return render(request, "user/dp.html")

def ldp(request):
    return render(request, "user/ldp.html")

def ldpaction(request):
    if request.method == "POST":
        age = request.POST.get("age")
        Gender = request.POST.get("Gender")
        Total_Bilirubin = request.POST.get("Total Bilirubin")
        Direct_Bilirubin = request.POST.get("Direct Bilirubin")
        Alkaline_Phosphotase = request.POST.get("Alkaline Phosphotase")
        Alamine_Aminotransferase = request.POST.get("Alamine Aminotransferase")
        Aspartate_Aminotransferase = request.POST.get("Aspartate Aminotransferase")
        Total_Protiens = request.POST.get("Total Protiens")
        Albumin = request.POST.get("ALB Albumin")
        Albumin_and_Globulin_Ratio = request.POST.get("Globulin Ratio")
        df = pd.read_csv('media/liver main.csv', encoding="latin1")
        df.columns = ['Age of the patient', 'Gender of the patient', 'Total Bilirubin',
        'Direct Bilirubin', 'Alkphos Alkaline Phosphotase',
        'Sgpt Alamine Aminotransferase', 'Sgot Aspartate Aminotransferase',
        'Total Protiens', 'ALB Albumin',
        'A/G Ratio Albumin and Globulin Ratio', 'Result']
        
        df["Age of the patient"] = df["Age of the patient"].fillna(df["Age of the patient"].mode()[0])
        df["Gender of the patient"] = df["Gender of the patient"].fillna(df["Gender of the patient"].mode()[0])
        df["Total Bilirubin"] = df["Total Bilirubin"].fillna(df["Total Bilirubin"].mean())
        df["Direct Bilirubin"] = df["Direct Bilirubin"].fillna(df["Direct Bilirubin"].mean())
        df["Alkphos Alkaline Phosphotase"] = df["Alkphos Alkaline Phosphotase"].fillna(df["Alkphos Alkaline Phosphotase"].mean())
        df["Sgpt Alamine Aminotransferase"] = df["Sgpt Alamine Aminotransferase"].fillna(df["Sgpt Alamine Aminotransferase"].mean())
        df["Sgot Aspartate Aminotransferase"] = df["Sgot Aspartate Aminotransferase"].fillna(df["Sgot Aspartate Aminotransferase"].mean())
        df["Total Protiens"] = df["Total Protiens"].fillna(df["Total Protiens"].mean())
        df["ALB Albumin"] = df["ALB Albumin"].fillna(df["ALB Albumin"].mean())
        df["A/G Ratio Albumin and Globulin Ratio"] = df["A/G Ratio Albumin and Globulin Ratio"].fillna(df["A/G Ratio Albumin and Globulin Ratio"].mean())

        df["Gender of the patient"] = df["Gender of the patient"].map({
            "Male": 1, "Female": 0
        })

        X = df.drop('Result', axis=1)
        y = df['Result']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        model = SVC(kernel='linear', C=1.0, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        custom_data = np.array([[age, Gender, Total_Bilirubin, Direct_Bilirubin, Alkaline_Phosphotase, Alamine_Aminotransferase, Aspartate_Aminotransferase, Total_Protiens, Albumin, Albumin_and_Globulin_Ratio]])
        custom_data_scaled = scaler.transform(custom_data)
        custom_predictions = model.predict(custom_data_scaled)
        print("Custom predictions:", custom_predictions)
        user_email = request.session.get('user_email')
        if custom_predictions == 1:
            prediction_message = "Liver Disease Detected"
            result_class = "result-detected"
            disease_type = "Liver Disease"
        else:
            prediction_message = "Liver Disease Not Detected"
            result_class = "result-not-detected"
            disease_type = "Liver Disease"
        ldpmodel(age=age, Gender=Gender, Total_Bilirubin=Total_Bilirubin, Direct_Bilirubin=Direct_Bilirubin, Alkaline_Phosphotase=Alkaline_Phosphotase, Alamine_Aminotransferase=Alamine_Aminotransferase, Aspartate_Aminotransferase=Aspartate_Aminotransferase, Total_Protiens=Total_Protiens, Albumin=Albumin, Albumin_and_Globulin_Ratio=Albumin_and_Globulin_Ratio, user_email=user_email, custom_predictions=custom_predictions).save()
        if user_email:
            subject = 'Liver Disease Prediction Result'
            from_email = settings.EMAIL_HOST_USER
            to_email = [user_email]
            html_content = render_to_string('user/email_template.html', {
                'prediction_message': prediction_message,
                'result_class': result_class,
                'disease_type': disease_type
            })
            msg = EmailMultiAlternatives(subject, '', from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        messages.success(request, prediction_message)
        return render(request, "user/ldp.html")
    else:
        return render(request, "user/ldp.html")

def puserredictions(request):
    return render(request, "user/predictions.html")

def hdpResults(request):
    user_email = request.session.get('user_email')
    data = hdpmodel.objects.filter(user_email=user_email)
    return render(request, "user/hdpresults.html", {'data': data})

def kdpResults(request):
    user_email = request.session.get('user_email')
    data = kdpmodel.objects.filter(user_email=user_email)
    return render(request, "user/kdpresults.html", {'data': data})

def bdpResults(request):
    user_email = request.session.get('user_email')
    data = bdpmodel.objects.filter(user_email=user_email)
    return render(request, "user/bdpresults.html", {'data': data})

def dpResults(request):
    user_email = request.session.get('user_email')
    data = dpmodel.objects.filter(user_email=user_email)
    return render(request, "user/dpresults.html", {'data': data})

def ldpResults(request):
    user_email = request.session.get('user_email')
    data = ldpmodel.objects.filter(user_email=user_email)
    return render(request, "user/ldpresults.html", {'data': data})


# user profile able to change username/ password
def userprofile(request):
    user_email = request.session.get('user_email')
    try:
        user_profile = pusermodel.objects.get(email=user_email)
    except pusermodel.DoesNotExist:
        user_profile = None
    return render(request, "user/userprofile.html", {'user_profile': user_profile})

def userprofileupdate(request):
    if request.method == "POST":
        new_username = request.POST.get("new-username")
        new_password = request.POST.get("new-password")
        user_email = request.session.get('user_email')
        user_profile = pusermodel.objects.get(email=user_email)
        if new_username:
            user_profile.name = new_username
        if new_password:
            user_profile.pswd = new_password
        user_profile.save()
        return render(request, "user/userprofile.html", {'user_profile': user_profile})
    else:
        return render(request, "user/userprofile.html")