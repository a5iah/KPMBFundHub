from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"), # index / welcomepage
    path("Login", views.Login, name="Login"), #login
    path("SignUp", views.SignUp, name="SignUp"), #SignUp
    path("HomePageUser/<str:userFirstName>", views.HomePageUser, name="HomePageUser"), #homepageU
    path("HomePageOrg/<str:orgName>", views.HomePageOrg, name="HomePageOrg"), #homepageO
    path('redirectHomePageUser', views.redirectHomePageUser, name='redirectHomePageUser'), #rHomepageU
    path('redirectHomePageOrg', views.redirectHomePageOrg, name='redirectHomePageOrg'), #rHomepageO
    path("DonationCampaignU", views.DonationCampaignU, name="DonationCampaignU"), #donationcampaignU
    path("DonationCampaignO", views.DonationCampaignO, name="DonationCampaignO"), #donationcampaignO
    path("donateU/<str:campaignID>", views.donateU, name="donateU"), #godonateU
    path("donateU/donationFormU/<str:campaignID>", views.donationFormU, name="donationFormU"), #donateformU
    path("CreateCampaignO", views.CreateCampaignO, name="CreateCampaignO"), #createcampaignO
    path("CampaignOrganizerU",views.CampaignOrganizerU, name="CampaignOrganizerU"), #campaignorgsU
    path("CampaignOrganizerO",views.CampaignOrganizerO, name="CampaignOrganizerO"), #campaignorgsO
    path("OrganizerRegistrationU", views.OrganizerRegistrationU, name="OrganizerRegistrationU"), #orgregistr --from user
    path("OrganizerRegistrationO", views.OrganizerRegistrationO, name="OrganizerRegistrationO"), #orgregistr --from org
    path("DashboardDonationUser", views.DashboardDonationUser, name="DashboardDonationUser"), #dbdonateU
    path("viewdeleteDonation/<str:donationID>", views.viewdeleteDonation, name="viewdeleteDonation"), #viewdeletedonationO
    path("viewdeleteDonation/deleteDonationData/<str:donationID>", views.deleteDonationData, name="deleteDonationData"), #deletedonationO
    path("DashboardCampaignOrg", views.DashboardCampaignOrg, name="DashboardCampaignOrg"), #dbcampaignO
    path("updateCampaign/<str:campaignID>", views.updateCampaign, name="updateCampaign"), #goupdatecampaignO
    path("updateCampaign/updateCampaignData/<str:campaignID>", views.updateCampaignData, name="updateCampaignData"), #updatecampaignO
    path("viewdeleteCampaign/<str:campaignID>", views.viewdeleteCampaign, name="viewdeleteCampaign"), #viewdeletecampaignO
    path("viewdeleteCampaign/deleteCampaignData/<str:campaignID>", views.deleteCampaignData, name="deleteCampaignData"), #deletecampaignO
    path("SeeDonorsO/<str:campaignID>", views.SeeDonorsO, name="SeeDonorsO"), #seedonorsO
    path("DashboardProfileUser", views.DashboardProfileUser, name="DashboardProfileUser"), #dbprofileU
    path("DashboardProfileOrg", views.DashboardProfileOrg, name="DashboardProfileOrg"), #dbprofileU
    path("updateProfileU/<str:userID>", views.updateProfileU, name="updateProfileU"), #goupdateprofileU
    path("updateProfileU/updateProfileDataU/<str:userID>", views.updateProfileDataU, name="updateProfileDataU"), #updateprofileU
    path("updateProfileO/<str:orgID>", views.updateProfileO, name="updateProfileO"), #goupdateprofileO
    path("updateProfileO/updateProfileDataO/<str:orgID>", views.updateProfileDataO, name="updateProfileDataO"), #updateprofileO
    path("LogOut", views.LogOut, name="LogOut"), #logout
]