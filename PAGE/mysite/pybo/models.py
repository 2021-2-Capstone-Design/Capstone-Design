from django.db import models


# Create your models here.


class DanceInfo(models.Model):  # information of every song
    song = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    content = models.TextField()  # coord info
    time = models.CharField(max_length=50)  # play time

    def __str__(self):
        return self.song + " - " + self.artist


class Team(models.Model):
    teamName = models.CharField(max_length=100)

    def __str__(self):
        return self.teamName


class TeamMember(models.Model):
    # Team 전체를 받는다
    teamName = models.ForeignKey(Team, on_delete=models.CASCADE)
    memberName = models.CharField(max_length=100)

    def __str__(self):
        return self.teamName.teamName + " - " + self.memberName


class Record(models.Model):  # record
    playerName = models.CharField(max_length=100)  # player name
    song = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    score = models.IntegerField()
    create_date = models.DateTimeField()
