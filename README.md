# CUED Part IA Flood Warning System

Solution to the Part IA Lent Term computing activity at the Department of
Engineering, University of Cambridge.

The activity is documented at
https://cued-partia-flood-warning.readthedocs.io/.


## Web Interface

```
bokeh serve main.py
```

### Map

![map](/docs/1.png)

The colour of each point depends on the relationship between the latest water level of that station and its typical range. Hover tool is also implemented, showing useful information when the mouse hovers above a datapoint.

![zoom_out](/docs/zoom_out.png)

Stations can be selected to display its historical water level data through clicking on the map or using the search box. Fuzzy matching is implemented for the search box.

![search](/docs/search.png)

### Prediction

High risk stations are displayed, and predicted for future change in water level.

![prediction](/docs/2.png)

The prediction is done both using a least-squared polynomial fit and a recurrent neural network. The LSTM network is trained on data obtained by a sliding window, and is applied recursively to predict future water levels.

![network](/docs/network.png)

### Warning

When considering the risk of flooding of a town, stations cannot be considered in isolation, so clustering is used on stations whose latest water level is 1.2 times its typical range above the upper typical range. The clustering algorithm implemented is DBSCAN with haversine distance as the distance matrix.

Then the town with the highest relative water level in each cluster is found, sorted using the mean relative water level of the cluster containing it.

![warning](/docs/3.png)



