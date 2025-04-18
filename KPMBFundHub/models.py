from django.db import models

# Create your models here.
class User (models.Model):
    userID = models.CharField(max_length=4, primary_key=True)
    userFirstName = models.TextField(max_length=50)
    userLastName = models.TextField(max_length=50)
    username = models.TextField(max_length=20, default='Ali')
    userPassword = models.TextField(max_length=50)
    userContactNum = models.CharField(max_length=11)
    userEmail = models.TextField(max_length=100)

    # autofill userID function
    def save(self, *args, **kwargs):
        if not self.userID:
            # Get total count of existing object in User table
            count = User.objects.count()+1
            # Generate userID with prefix 'U' and zero padding
            self.userID = 'U' + '{:03d}'.format(count)
        super().save(*args, **kwargs)

class Organizer (models.Model):
    orgID = models.CharField(max_length=4, primary_key=True)
    orgName = models.TextField(max_length=50)
    orgPassword = models.TextField(max_length=50)
    orgContactNum = models.TextField(max_length=50)
    orgDesc = models.TextField(max_length=500)

    # autofill orgID function
    def save(self, *args, **kwargs):
        if not self.orgID:
            # Get total count of existing object in User table
            count = Organizer.objects.count()+1
            # Generate userID with prefix 'U' and zero padding
            self.orgID = 'O' + '{:03d}'.format(count)
        super().save(*args, **kwargs)


class Campaign (models.Model):
    campaignID = models.CharField(max_length=4, primary_key=True)
    campaignName = models.TextField(max_length=50)
    campaignDesc = models.TextField(max_length=500)
    orgID = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    targetAmount_RM = models.DecimalField(max_digits=10, decimal_places=2)
    numOfDonors = models.IntegerField(default=0)
    startDate = models.DateField()
    endDate = models.DateField()

    # autofill campaignID function
    def save(self, *args, **kwargs):
        if not self.campaignID:
            # Get total count of existing object in User table
            count = Campaign.objects.count()+1
            # Generate userID with prefix 'U' and zero padding
            self.campaignID = 'C' + '{:03d}'.format(count)
        super().save(*args, **kwargs)

class Donation (models.Model):
    donationID = models.CharField(max_length=4, primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    campaignID = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    amountDonated_RM = models.DecimalField(max_digits=10, decimal_places=2)
    paymentMethod = models.TextField(max_length=20)
    dateNtime = models.DateTimeField()
    paymentStatus = models.TextField(max_length=50, default="Success")

    # autofill donationID function
    def save(self, *args, **kwargs):
        if not self.donationID:
            # Get total count of existing object in User table
            count = Donation.objects.count()+1
            # Generate userID with prefix 'U' and zero padding
            self.donationID = 'D' + '{:03d}'.format(count)
        super().save(*args, **kwargs)