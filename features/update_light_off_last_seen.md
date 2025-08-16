Update all of the light off at switch sensors to only calculate state based on 15 mins since last seen.

``` jinja
{{states('sensor.coat_closet_hall_last_seen')}}
```