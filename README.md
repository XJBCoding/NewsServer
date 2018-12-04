# News Server

## About...

## Development
```
pip install -r requirements/dev.txt
```

## Testing
For pre-commit testing, set it up like so:
```
./bin/git-hooks/hook-setup.sh
```
The process for commiting is as follows:
```
git checkout master
# Develop on master branch
git commit                  # The pre-commit will run

git checkout logs
git add logs
git commit
git push                    # This will push to the remote branch origin/logs

git checkout master
git push                    # This will push to the remote branch origin/master
```

For post-commit CI, we use [Travis](https://travis-ci.com/XJBCoding/NewsServer).
