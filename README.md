# donation-tracker
Donation tracking for pitchers during fund drive. Scrapes data from [Allegiance's donation dashboard](https://michiganradio.secureallegiance.com/wuom/DonationTracker/SelectCampaign.aspx#61;WINTER22) and writes to [this Google sheet](https://docs.google.com/spreadsheets/d/1uP3oVj6WAJ61DmCkkjIv_9SmFCEm59-okOVusFL1FMs/edit#gid=984305523).

### steps to run a drive
1. Create a new drive in the key file at `/mnt/disks/home/donation-tracker/drive_keys.json`. Should look something like this:
```{
  ...,
  "spring_2023": {
    "drive": "SPRING 2023 RADIO DRIVE",
    "pw": "SD2023",
    "start_date": "2023-03-13",
    "end_date": "2023-03-18"
  },
  ...
}
```
2. Run new drive task to create files and directories, like this for the above key:
```
python donation-tracker.py --task new --drive spring_2023
```
3. Update `run_donation_tracker` bash script to point at the correct drive.
```
cd /home/bgowland/donation-tracker/
. venv/bin/activate
python donation_tracker.py --task update --drive spring_2023 <<--- this
deactivate
```
4. When you're ready to start tracking, update the crontab. There should be a line to comment out, but it should look like this:
```
*/2 * * * . /home/bgowland/donation-tracker/run_donation_tracker
```
5. Let the drive run, there's a log file at `/mnt/disks/home/logs/donation_tracker_yyyy-mm-dd.log` if you need to check on the code. It should fail ~1 or 2 times daily (which out of 720 daily runs is not a big deal).
6. When you're done with a drive - copy and save the contents of the Donation Tracker workbook to a new workbook with the date appended to the name. Kill the cron task, and you're done :+1:
