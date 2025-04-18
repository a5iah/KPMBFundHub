from django.shortcuts import render
from KPMBFundHub.models import User, Organizer, Campaign, Donation
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.utils import timezone

# Create your views here.

# index --WelcomePage
def index(request):
    return render (request, "index.html")

# SignUp function --for normal user
def SignUp(request):
    if request.method == 'POST':
        userFirstName = request.POST['userFirstName']
        userLastName = request.POST['userLastName']
        username = request.POST['username']
        userContactNum = request.POST['userContactNum']
        userEmail = request.POST['userEmail']
        userPassword = request.POST['userPassword']
        confirmPassword = request.POST['confirmPassword']
        if userPassword == confirmPassword:
            userData = User(
                userFirstName=userFirstName, 
                userLastName=userLastName, 
                username = username,
                userContactNum=userContactNum, 
                userEmail = userEmail, 
                userPassword=userPassword)
            userData.save()
            return redirect('Login')
        else:
            dict = {
                'message':'Password entered is not match'
            }
            return render(request, 'SignUp.html', dict)
    else:
        dict = {
            'message':''
        }
        return render(request, 'SignUp.html',dict)
    
# Login function --for normal user and organizer
def Login(request):
    if request.method == 'POST':
        logintype = request.POST['logintype']
        username = request.POST['username']
        password = request.POST['password']
        if logintype == 'user':
            # find username in User table
            find = User.objects.filter(username=username).values()
            if find.exists():
                if(find[0]['userPassword'] == password):
                    # Store the user's ID in session for later use
                    request.session['userID'] = find[0]['userID']  # Save userID in session
                    # Store the username in session after successful login
                    request.session['username'] = find[0]['username']
                    return redirect(reverse('HomePageUser', args=[find[0]['username']]))
                else:
                     dict={
                          'message':'wrong password'
                     }
                     return render (request, 'Login.html', dict)
            else:
                 dict = {
                      'message' : 'wrong username'
                 }
                 return render (request, 'Login.html', dict)
        elif logintype == 'org':
            # find username in Organizer table
            find = Organizer.objects.filter(orgName=username).values()
            if find.exists():
                if(find[0]['orgPassword'] == password):
                    # Store the orgName (which acts like a username) in the session
                    request.session['orgID'] = find[0]['orgID']  # Save orgID in session
                    request.session['orgName'] = find[0]['orgName']
                    return redirect(reverse("HomePageOrg", args=[find[0]['orgName']]))
                else:
                     dict={
                          'message':'wrong password'
                     }
                     return render (request, 'Login.html', dict)
            else:
                 dict = {
                      'message' : 'wrong username'
                 }
                 return render (request, 'Login.html', dict)
        else:
            dict = {
                'message':'Please enter username and password'
            }    
            return render(request, 'Login.html', dict)
    else:
         dict = {
              'message' : ''
         }
         return render (request, 'Login.html', dict)
    
# HomePage function -- normal user
def HomePageUser(request, userFirstName):
    # Retrieve the userID from the session
    userID = request.session.get('userID', None) 
    
    if userID:
        # Find the user object using userID
        user = User.objects.get(userID=userID)
        # Retrieve the username (or name)
        userFirstName = user.userFirstName  # Assuming 'username' is the user's name
        dict = {
            'userFirstName': userFirstName
        }
        return render (request, "HomePageUser.html", dict)
    else:
        return redirect ("Login") # Redirect to kalau tak logged in

# function to redirect to HomePageUser -- normal user
def redirectHomePageUser(request):
    userID = request.session.get('userID', None)

    if userID:
        user = User.objects.get(userID=userID)
        userFirstName = user.userFirstName
        return redirect('HomePageUser', userFirstName)
    else:
        return redirect("Login")
    
# HomePageOrg function -- org
def HomePageOrg(request, orgName):
    orgID = request.session.get('orgID', None)

    if orgID:
        org = Organizer.objects.get(orgID=orgID)
        orgName = org.orgName 
        dict = {
            'orgName': orgName,
        }
        return render (request, "HomePageOrg.html", dict)
    else:
        return redirect ("Login")

# function to redirect to HomePageOrg -- org
def redirectHomePageOrg(request):
    orgID = request.session.get('orgID', None)

    if orgID:
        org = Organizer.objects.get(orgID=orgID)
        orgName = org.orgName
        return redirect('HomePageOrg', orgName)
    else:
        return redirect("Login")

# Donation Campaign -- normal user
def DonationCampaignU(request):
    query = request.GET.get('searchCampaign')  # Get search query from the form
    message = ''
    userID = request.session.get('userID', None)
    
    if query:
        # Search based on campaignID or campaignName
        findCampaign = Campaign.objects.filter(
            Q(campaignID__icontains=query) | Q(campaignName__icontains=query)
        ).select_related('orgID')
        
        if not findCampaign:  # If no results are found
            message = 'Sorry, no campaign found :('
    
    else:
        # Show all campaigns when no search query is provided
        findCampaign = Campaign.objects.all().select_related('orgID')

    dict = {
        'findCampaign': findCampaign,
        'message': message,
        'userID': userID,
    }

    return render(request, 'DonationCampaignU.html', dict)

# Donation Campaign -- org
def DonationCampaignO(request):
    query = request.GET.get('searchCampaign')  # Get search query from the form
    message = ''
    orgID = request.session.get('orgID', None)
    
    if query:
        # Search based on campaignID or campaignName
        findCampaign = Campaign.objects.filter(
            Q(campaignID__icontains=query) | Q(campaignName__icontains=query)
        ).values().select_related('orgID')
        
        if not findCampaign:  # If no results are found
            message = 'Sorry, no campaign found :('
    
    else:
        # Show all campaigns when no search query is provided
        findCampaign = Campaign.objects.all().select_related('orgID')

    dict = {
        'findCampaign': findCampaign,
        'message': message,
        'orgID': orgID,
    }

    return render(request, 'DonationCampaignO.html', dict)

# donateU function -- normal user
def donateU(request, campaignID):
    userID = request.session.get('userID', None)
    # Get campaignID
    campaignID = Campaign.objects.get(campaignID=campaignID)
    dict = {
        'campaignID':campaignID,
        'message':'You are donating to ',
        'userID': userID,
    }
    return render(request,'DonateFormU.html',dict)

# donationFormU function -- normal user
def donationFormU(request,campaignID):
    userID = request.session.get('userID', None)
    user = User.objects.get(userID=userID)
    campaign = Campaign.objects.get(campaignID=campaignID)
    if request.method == 'POST':
        amountDonated_RM = request.POST['amount']
        paymentMethod = request.POST['paymentMethod']

        donation = Donation (
            userID = user,
            campaignID = campaign,
            amountDonated_RM = amountDonated_RM,
            paymentMethod = paymentMethod,
            dateNtime = timezone.now(),
            paymentStatus = 'Success'
        )
        donation.save()

        return HttpResponseRedirect(reverse('DashboardDonationUser'))
    dict = {
        'campaignID': campaign,
        'campaignName': campaign.campaignName, 
        'userID': user.userID,
    }
    return render(request, 'DonateFormU.html', dict)

# CreateCampaignO -- org
def CreateCampaignO(request):
    orgID = request.session.get('orgID', None)
    org = Organizer.objects.get(orgID=orgID)
    if request.method == 'POST':
        campaignName = request.POST['campaignName']
        campaignDesc = request.POST['campaignDesc']
        targetAmount_RM = request.POST['targetAmount_RM']
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']

        campaign = Campaign (
            campaignName = campaignName,
            campaignDesc = campaignDesc,
            orgID = org,
            targetAmount_RM = targetAmount_RM,
            numOfDonors = 0,
            startDate = startDate,
            endDate = endDate,
        )
        campaign.save()

        return HttpResponseRedirect(reverse('DashboardCampaignOrg'))
    dict = {
        'org': org,
    }
    return render(request, 'CreateCampaignO.html', dict)

# CampaignOrganizerU function -- normal user
def CampaignOrganizerU(request):
    query = request.GET.get('searchOrganizer')  # Get search query from the form
    message = ''
    userID = request.session.get('userID', None)
    
    if query:
        # Search based on campaignID or campaignName
        findOrganizer = Organizer.objects.filter(
            Q(orgID__icontains=query) | Q(orgName__icontains=query)
        ).values()
        
        if not findOrganizer:  # If no results are found
            message = 'Sorry, no organizer found :('
    
    else:
        # Show all campaigns when no search query is provided
        findOrganizer = Organizer.objects.all().values()

    dict = {
        'findOrganizer': findOrganizer,
        'message': message,
        'userID': userID,
    }

    return render(request, 'CampaignOrganizerU.html', dict)

# CampaignOrganizerO function -- org
def CampaignOrganizerO(request):
    query = request.GET.get('searchOrganizer')  # Get search query from the form
    message = ''
    orgID = request.session.get('orgID', None)
    
    if query:
        # Search based on campaignID or campaignName
        findOrganizer = Organizer.objects.filter(
            Q(orgID__icontains=query) | Q(orgName__icontains=query)
        ).values()
        
        if not findOrganizer:  # If no results are found
            message = 'Sorry, no organizer found :('
    
    else:
        # Show all campaigns when no search query is provided
        findOrganizer = Organizer.objects.all().values()

    dict = {
        'findOrganizer': findOrganizer,
        'message': message,
        'orgID': orgID,
    }

    return render(request, 'CampaignOrganizerO.html', dict)

# Organizer Registration -- normal user
def OrganizerRegistrationU(request):
    if request.method == 'POST':
        orgName = request.POST['orgName']
        orgContactNum = request.POST['orgContactNum']
        orgDesc = request.POST['orgDesc']
        orgPassword = request.POST['orgPassword']
        confirmPassword = request.POST['confirmPassword']
        if orgPassword == confirmPassword:
            orgData = Organizer(
                orgName=orgName, 
                orgContactNum=orgContactNum, 
                orgDesc = orgDesc, 
                orgPassword=orgPassword)
            orgData.save()
            dict = {
                'message':'Organizer Registration is Successful!',
                # to display link to user and redirect them to Login page
                'link':'Click here to login as organizer',
                'login_url': reverse('Login')
            }
            return render(request, 'OrganizerRegistrationU.html', dict)
        else:
            dict = {
                'message':'Password entered is not match'
            }
            return render(request, 'OrganizerRegistrationU.html', dict)
    else:
        dict = {
            'message':''
        }
        return render(request, 'OrganizerRegistrationU.html',dict)
    
# Organizer Registration -- org
def OrganizerRegistrationO(request):
    if request.method == 'POST':
        orgName = request.POST['orgName']
        orgContactNum = request.POST['orgContactNum']
        orgDesc = request.POST['orgDesc']
        orgPassword = request.POST['orgPassword']
        confirmPassword = request.POST['confirmPassword']
        if orgPassword == confirmPassword:
            orgData = Organizer(
                orgName=orgName, 
                orgContactNum=orgContactNum, 
                orgDesc = orgDesc, 
                orgPassword=orgPassword)
            orgData.save()
            dict = {
                'message':'Organizer Registration is Successful!',
                # to display link to user and redirect them to Login page
                'link':'Click here to login as organizer',
                'login_url': reverse('Login')
            }
            return render(request, 'OrganizerRegistrationO.html', dict)
        else:
            dict = {
                'message':'Password entered is not match'
            }
            return render(request, 'OrganizerRegistrationO.html', dict)
    else:
        dict = {
            'message':''
        }
        return render(request, 'OrganizerRegistrationO.html',dict)

# DashboardDonationUser -- normal user
def DashboardDonationUser(request):
    userID = request.session.get('userID', None)
    user = User.objects.get(userID=userID)
    displayDonations = Donation.objects.select_related('campaignID').filter(userID=userID)
    dict = {
        'displayDonations' : displayDonations,
        'userFirstName': user.userFirstName,
        'userID' : userID,
    }
    return render(request, 'DashboardDonationUser.html', dict)

# viewdeleteDonation function -- normal user
def viewdeleteDonation(request,donationID):
    userID = request.session.get('userID', None)
    user = User.objects.get(userID=userID)
    donation = Donation.objects.get(donationID=donationID)
    deleteID = Donation.objects.get(donationID=donationID)
    dateNtime = deleteID.dateNtime.strftime('%Y-%m-%d %H:%M')
    dict={
        'deleteID':deleteID,
        'donationID':donation.donationID,
        'dateNtime': dateNtime,
        'userFirstName':user.userFirstName,
        'userID' : userID
    }
    return render(request,"DeleteDonationU.html", dict)

# deleteDonationData function -- normal user
def deleteDonationData(request,donationID):
    deleteDonation=Donation.objects.get(donationID=donationID)
    deleteDonation.delete()
    return HttpResponseRedirect(reverse("DashboardDonationUser"))

# DashboardProfileUser function -- normal user
def DashboardProfileUser(request):
    userID = request.session.get('userID', None)
    user = User.objects.get(userID=userID)
    displayUserProfile = User.objects.filter(userID=userID)
    dict = {
        'displayUserProfile' : displayUserProfile,
        'userFirstName': user.userFirstName,
        'userID' : userID,
    }
    return render(request, 'DashboardProfileUser.html',dict)

# updateProfileU function -- normal user
def updateProfileU(request,userID):
    userID = request.session.get('userID', None)
    user = User.objects.get(userID=userID)
    updateID = User.objects.get(userID=userID)
    dict={
        'updateID':updateID,
        'userFirstName': user.userFirstName,
        'userID' : userID
    }
    return render(request,"UpdateProfileUser.html",dict)

# updateProfileDataU function -- normal user
def updateProfileDataU(request,userID):
    userID = request.session['userID']
    userData = User.objects.get(userID=userID)
    userFirstName = request.POST['userFirstName']
    userLastName = request.POST['userLastName']
    username = request.POST['username']
    userEmail = request.POST['userEmail']
    userContactNum = request.POST['userContactNum']
    userPassword = request.POST['userPassword']
    confirmPassword = request.POST['confirmPassword']
    if userPassword == confirmPassword:
        userData.userID = userID
        userData.userFirstName = userFirstName
        userData.userLastName = userLastName
        userData.username = username
        userData.userEmail = userEmail
        userData.userContactNum = userContactNum
        userData.userPassword = userPassword
        userData.save()
        dict = {
            'message':'Update Profile Data is Successful!',
        }
        return HttpResponseRedirect(reverse("DashboardProfileUser"), dict)
    else:
        dict = {
            'userData': userData,
            'message':'Password entered is not match'
        }
        return render(request, 'UpdateProfileUser.html', dict)
    
# DashboardProfileOrg function -- org
def DashboardProfileOrg(request):
    orgID = request.session.get('orgID', None)
    org = Organizer.objects.get(orgID=orgID)
    displayOrgProfile = Organizer.objects.filter(orgID=orgID)
    dict = {
        'displayOrgProfile' : displayOrgProfile,
        'orgName': org.orgName
    }
    return render(request, 'DashboardProfileOrg.html',dict)

# updateProfileO function -- org
def updateProfileO(request,orgID):
    orgID = request.session.get('orgID', None)
    org = Organizer.objects.get(orgID=orgID)
    updateID = Organizer.objects.get(orgID=orgID)
    dict={
        'updateID':updateID,
        'orgName': org.orgName,
        'orgID' : orgID
    }
    return render(request,"UpdateProfileOrg.html",dict)

# updateProfileDataO function -- org
def updateProfileDataO(request,orgID):
    orgID = request.session['orgID']
    orgData = Organizer.objects.get(orgID=orgID)
    orgName = request.POST['orgName']
    orgContactNum = request.POST['orgContactNum']
    orgDesc = request.POST['orgDesc']
    orgPassword = request.POST['orgPassword']
    confirmPassword = request.POST['confirmPassword']
    if orgPassword == confirmPassword:
        orgData.orgID = orgID
        orgData.orgName = orgName
        orgData.orgContactNum = orgContactNum
        orgData.orgDesc = orgDesc
        orgData.orgPassword = orgPassword
        orgData.save()
        dict = {
            'message':'Update Profile Data is Successful!',
        }
        return HttpResponseRedirect(reverse("DashboardProfileOrg"), dict)
    else:
        dict = {
            'orgData': orgData,
            'message':'Password entered is not match'
        }
        return render(request, 'UpdateProfileOrg.html', dict)

# DashboardCampaignOrg function -- org
def DashboardCampaignOrg(request):
    orgID = request.session.get('orgID', None)
    org = Organizer.objects.get(orgID=orgID)
    displayCampaigns = Campaign.objects.filter(orgID_id=orgID)
    dict = {
        'displayCampaigns' : displayCampaigns,
        'orgName': org.orgName,
        'orgID': orgID,
    }
    return render(request, 'DashboardCampaignOrg.html',dict)

# updateCampaign function -- org
def updateCampaign(request,campaignID):
    orgID = request.session.get('orgID', None)
    org = Organizer.objects.get(orgID=orgID)
    campaign = Campaign.objects.get(campaignID=campaignID)
    updateID = Campaign.objects.get(campaignID=campaignID)
    startDate = updateID.startDate.strftime('%Y-%m-%d')
    endDate = updateID.endDate.strftime('%Y-%m-%d')
    dict={
        'updateID':updateID,
        'startDate': startDate,
        'endDate': endDate,
        'campaignName':campaign.campaignName,
        'orgName' : org.orgName,
        'orgID' : orgID
    }
    return render(request,"UpdateCampaignO.html",dict)

# updateCampaignData function -- org
def updateCampaignData(request,campaignID):
    orgID = request.session.get('orgID', None)
    campaignData = Campaign.objects.get(campaignID=campaignID)
    campaignName = request.POST['campaignName']
    campaignDesc = request.POST['campaignDesc']
    targetAmount_RM = request.POST['targetAmount_RM']
    startDate = request.POST['startDate']
    endDate = request.POST['endDate']

    campaignData.campaignID = campaignID
    campaignData.campaignName = campaignName
    campaignData.campaignDesc = campaignDesc
    campaignData.orgID_id = orgID
    campaignData.targetAmount_RM = targetAmount_RM
    campaignData.startDate = startDate
    campaignData.endDate = endDate
    campaignData.save()
    dict = {
        'message':'Update Campaign Data is Successful!',
    }
    return HttpResponseRedirect(reverse("DashboardCampaignOrg"), dict)
    
# viewdeleteCampaign function -- org
def viewdeleteCampaign(request,campaignID):
    orgID = request.session.get('orgID', None)
    org = Organizer.objects.get(orgID=orgID)
    campaign = Campaign.objects.get(campaignID=campaignID)
    deleteID = Campaign.objects.get(campaignID=campaignID)
    startDate = deleteID.startDate.strftime('%Y-%m-%d')
    endDate = deleteID.endDate.strftime('%Y-%m-%d')
    dict={
        'deleteID':deleteID,
        'startDate': startDate,
        'endDate': endDate,
        'campaignName':campaign.campaignName,
        'orgName' : org.orgName,
        'orgID' : orgID
    }
    return render(request,"DeleteCampaignO.html", dict)

# deleteCampaignData function -- org
def deleteCampaignData(request,campaignID):
    deleteCampaign=Campaign.objects.get(campaignID=campaignID)
    deleteCampaign.delete()
    return HttpResponseRedirect(reverse("DashboardCampaignOrg"))

# seeDonors
def SeeDonorsO(request,campaignID):
    orgID = request.session.get('orgID', None)
    org = Organizer.objects.get(orgID=orgID)
    campaign = Campaign.objects.get(campaignID=campaignID)
    displayDonors = Donation.objects.select_related('userID').filter(campaignID_id=campaignID)
    dict = {
        'displayDonors' : displayDonors,
        'campaignName':campaign.campaignName,
        'orgName' : org.orgName,
        'orgID': orgID
    }
    return render(request, 'SeeDonorsO.html',dict)

# LogOut function --for normal user and org
def LogOut(request):
    request.session.flush() # This clears all session data to log out user
    return HttpResponseRedirect(reverse("index"))