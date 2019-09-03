"""
Google POI Scraper helper Class
Created in September, 2019
@author: Yunbo Chen
"""
import os

# To test if grid is small enough
SMALLEST_GRID_SIZE = 0.000006
SIDE_LENGTH = 0.0026

class CoordBound():
    def __init__(self, swlat, swlng, nelat, nelng):
        self.sw_lat = swlat
        self.sw_lng = swlng
        self.ne_lat = nelat
        self.ne_lng = nelng
        self.width = abs(self.ne_lng-self.sw_lng)
        self.height = abs(self.ne_lat-self.sw_lat)

    def __str__(self):
        return "sw_lat, sw_lng, ne_lat, ne_lng: {}, {}, {}, {}\n".format(self.sw_lat, self.sw_lng, self.ne_lat, self.ne_lng)

    def __repr__(self):
        return "sw_lat, sw_lng, ne_lat, ne_lng: {}, {}, {}, {}\n".format(self.sw_lat, self.sw_lng, self.ne_lat, self.ne_lng)

    def serialize(self):
        return {
            'sw_lat': self.sw_lat, 
            'sw_lng': self.sw_lng,
            'ne_lat': self.ne_lat,
            'ne_lng': self.ne_lng
        }

    def get_size(self):
        return self.height*self.width

    def cross_cut(self):
        center = (self.sw_lat+self.height/2, self.sw_lng+self.width/2)
        ret = []
        ret.append(CoordBound(self.sw_lat, self.sw_lng, center[0], center[1]))
        ret.append(CoordBound(center[0], self.sw_lng, self.ne_lat, center[1]))
        ret.append(CoordBound(self.sw_lat, center[1], center[0], self.ne_lng))
        ret.append(CoordBound(center[0], center[1], self.ne_lat, self.ne_lng))
        return ret

    def para_cut(self):
        ret = []
        # 找出长边
        if (self.height > self.width):
            for i in range(4):
                ret.append(CoordBound(self.sw_lat+i*height/4, self.sw_lng, self.sw_lat+(i+1)*height/4, self.ne_lng))
        else:
            for i in range(4):
                ret.append(CoordBound(self.sw_lat, self.sw_lng+i*self.width/4, self.ne_lat, self.sw_lng+(i+1)*self.width/4))
        return ret

    def one_to_four(self):
        # check height/width ratio
        if max(self.height, self.width)/ min(self.height, self.width) >= 4:
            # go for parallelized cut
            return self.para_cut()
        else:
            return self.cross_cut()

    def divide_side(self, start, goal):
        ret = []
        i = 0
        while (start < goal):
            ret.append(start)
            start += SIDE_LENGTH
        ret.append(goal)
        return ret
    
    def dividify(self):
        grids = []
        lat_pts = self.divide_side(self.sw_lat, self.ne_lat)
        lng_pts = self.divide_side(self.sw_lng, self.ne_lng)
        for i in range(len(lat_pts)-1):
            for j in range(len(lng_pts)-1):
                grids.append(CoordBound(
                    lat_pts[i], lng_pts[j], lat_pts[i+1], lng_pts[j+1]
                ))
        return grids
        # old 1->4 division algorithm
        # grids = [self]
        # while grids[0].get_size() > SMALLEST_GRID_SIZE:
        #     temp = []
        #     for grid in grids:
        #         temp += grid.one_to_four()
        #     grids = temp
        # return grids

