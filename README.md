# Crover-Technical-Challenge

A live demo of the app is deployed on Heroku and can be accessed [here.](https://crover-technical-challenge-bcj.herokuapp.com/)

## How to run the app locally

The app can be run locally by cloning the repository through the following steps:

1. Navigate to the repository page on [GitHub.](https://github.com/bob134552/Crover-Technical-Challenge)

2. Above the files in the top right corner click on the "Code" button.

3. Copy the link shown.

4. In your IDE open the command line and type `git clone` followed by the copied url from before.

5. Press enter to create a local clone of the repository.

### Requirements

A virtual environment is required and can be set up with the command `python -m venv .venv` or `python3 -m venv .venv` if on macOS/Linux. Once the virtual environment is set up run it by copying the activate path and executing it in the terminal `C:\Users\<USERNAME>\<PATH>\<TO>\<VENEV>\venv\Scripts\Activate.ps1`.

Once running use `pip install -r requirements.txt` in your terminal to install all required packages for the app.

### Database

Locally a sqlite3 database is used but when deployed on heroku a PostgreSQL database is used.
For both, initial migrations are required to be run using the command `python manage.py migrate` to apply all migrations.

Additionally, any updates to the models in the database require for migrations to be run using the commands `python manage.py makemigrations` followed by `python manage.py migrate` and a superuser is required which is created using the command `python manage.py createsuperuser`.

#### TempData Model

|Name|Key|Description|Field Type|
|:---|:----:|:----:|---:|
|Set|set|max_length=255|CharField|
|X point|x_point||FloatField|
|Y point|y_point||FloatField|
|Temperature|temperature||FloatField|



### Technologies used

- [HTML5](https://en.wikipedia.org/wiki/HTML)
- [CSS](https://en.wikipedia.org/wiki/CSS)
- [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
- [Python](https://en.wikipedia.org/wiki/Python_(programming_language))
- [jQuery](https://en.wikipedia.org/wiki/JQuery)
- [Bootstrap5](https://getbootstrap.com/)
- [Heroku](https://www.heroku.com/)
  - Used for deploying and managing the project.
  - Postgres database used outside of developement.
- [GitHub](https://github.com/)
  - Used to store the projects code.
- [VSCode](https://code.visualstudio.com/)
  - IDE used to build the site.
- [SQLite3](https://www.sqlite.org/index.html)
  - For database management during developement.
- [Plotly](https://plotly.com/)
  - To plot the graphs shown on the app.

## Work Description

After the initial set up of the app, I looked up methods to upload the data sets from the provided csv files. In my first attempt I followed the instructions in [this](https://stackoverflow.com/questions/2459979/how-to-import-csv-data-into-django-models) stackoverflow answer but found that due to the large amount of data in the csv file that creating each data entry into the django model was taking far too long. I then found [this article](https://ramramesh1374.medium.com/upload-csv-using-django-bulk-create-c75b28fc19f0) and adapted the code to suite my needs.

Once the initial problem of uploading the data from the provided csv files was working correctly, it was required to plot the temperature at specific points on a plot. I was not sure on how to plot graphs before but from looking around I found [Plotly](https://plotly.com/). After reading through the documentation and some [examples](https://stackoverflow.com/questions/36846395/embedding-a-plotly-chart-in-a-django-template) on stackoverflow I was able to confidently create a customized interactive graph to display on the app.

Additionally I added some javascript that would reload the app if a new data set was selected from the dropdown options and a way to delete the selected set with a modal to ensure user is sure about deleting the data set.

### Order work was carried out

1. Create virtual environment and install django along with all other required packages.

2. Migrate the database and create superuser.

3. Create TempData model and create a basic view to display the home app index.html template that extends from a base.  html template.

4. Display a user input in index.html template for csv files to be uploaded.

5. Expand home view to handle post requests of csv files and bulk create DataTemp model entries.

6. Find a way to plot the imported data and separate the data to their respective set.

7. Display plotted graph in index.html below the input for csv files.

8. Find a way to display positions x and y when hovering over each data point.

9. Allow to swap graphs to different data sets (set selector).

10. Allow user to delete a selected data set if they were sure(delete button and modal asking for confirmation).

11. Deploy a working demo to heroku.

### Problems encountered

- After deployment to Heroku uploading the csv file didn't work.
  - This problem was fixed by moving the whole POST method in the home view to the top of the view.

- Altering the hover tooltip data when hovering over a data point.
  - This problem was solved from searching the documentation for Plotly [here.](https://plotly.com/python/hover-text-and-formatting/)

- Duplicate upload for a data set was being allowed.
  - This was prevented by adding the following to prevent a duplicate upload:

```
if TempData.objects.filter(set=csv_file.name.split('.csv')[0]).exists():
            messages.error(request, 'This data set already exists.')
            return redirect('home')
```

- Due to the amount of data points app may not function correctly on mobile displays smaller than a tablet.

## Images of app

<img src="example_images\data-set-0.png" alt="example graph of data_0">
Above example of the graph for data_0.csv.

\
<img src="example_images\example-dropdown.png" alt="example dropdown">
Example of the dropdown menu to select different data sets (Adds more options when more data sets are uploaded).

\
<img src="example_images\zoomed-and-selected-data-point.png" alt="zoomed in graph example with hover data.">
Example of a data point displaying temperature, both positions(x, y) and its number in the list.

\
<img src="example_images\delete-prompt.png" alt="example delete prompt">
Example of a delete prompt to ensure that user doesn't accidentally delete a dataset.
