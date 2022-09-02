import re
from datetime import datetime


def _get_latest_backups(prune_logfilename):
    archive_line = re.compile(r'\d{8}_\d{4}\s+\w{3}, (\d{4})-(\d\d)-(\d\d) [\d,:]* \[\w*\]')
    title_line = re.compile(r'\d{8}_\d{4} - Current backup list for \/([\w,\/]+)\/(\w+)')

    latest_backups = {}
    current_backup = None
    with open(prune_logfilename) as f:
        for line in f:
            line = line.strip()
            if current_backup is None:
                title_match = title_line.match(line)
                if title_match:
                    current_backup = (title_match.group(1), title_match.group(2))
                    latest_backups[current_backup] = []
            else:
                archive_match = archive_line.match(line)
                if archive_match is None:
                    current_backup = None
                else:
                    year,month,day = [int(archive_match.group(i)) for i in [1,2,3]]
                    latest_backups[current_backup].append(datetime(year,month,day))
    return latest_backups

def are_backups_ok(prune_logfilename):
    latest_backups = _get_latest_backups(prune_logfilename)
    targets = ['internal_backup', 'external_backup/backups']
    max_age = [1.5, 8] # days
    max_age = [m*3600*24 for m in max_age] # seconds
    repos = ['data', 'nextcloud_data', 'rest']
    for m,t in zip(max_age,targets):
        for r in repos:
            if (t,r) not in latest_backups:
                return False, f"Missing backup: {t}/{r}"
            if len(latest_backups[(t,r)]) == 0:
               return False, "Error parsing backup logfile"
            age = (datetime.now() - latest_backups[(t,r)][-1]).total_seconds()
            if age > m:
                return False, f"Backup too old: {t}/{r}; Age = {age/(3600*24):.1f} days"
    return True, "Ok"

if __name__ == '__main__':
    backup_status, msg = are_backups_ok('data/prune.log')
    print(msg)
