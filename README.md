# Owkin test project

To run this project you must run the following commands:

```
git clone https://github.com/thomasrosnet/owkin-test.git
cd owkin-test/data-curation
sudo apt-get install python3.10-venv
python3.10 -m venv owkin-env
source owkin-env/bin/activate
pip install -r requirements.txt
./launch_dev.sh
```

## /!\ Important

Make sure you place the data CSV file in the "data" folder.

The test data file is not commited to the Github repository !

For the moment the code generate the Web UI using only the first file listed in the "data" folder.
