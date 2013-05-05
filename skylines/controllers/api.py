# -*- coding: utf-8 -*-
from tg import expose
from tg.i18n import ugettext as _
from webob.exc import HTTPBadRequest

from .base import BaseController
from skylines.model import Airspace, MountainWaveProject, Location
from skylines.lib.string import isnumeric

__all__ = ['APIController']


class APIController(BaseController):
    @expose('json')
    def index(self, **kwargs):
        return dict(self.airspace(**kwargs).items() +
                    self.mountain_wave_project(**kwargs).items())

    @expose('json')
    def airspace(self, **kwargs):
        try:
            latitude = float(kwargs['lat'])
            longitude = float(kwargs['lon'])

        except (KeyError, ValueError):
            raise HTTPBadRequest

        location = Location(latitude=latitude,
                            longitude=longitude)

        airspaces = Airspace.get_info(location)
        info = []

        for airspace in airspaces:
            info.append(dict(name=airspace.name,
                             base=airspace.base,
                             top=airspace.top,
                             airspace_class=airspace.airspace_class,
                             country=airspace.country_code))

        return dict(airspaces=info)

    @expose('json')
    def mountain_wave_project(self, **kwargs):
        try:
            latitude = float(kwargs['lat'])
            longitude = float(kwargs['lon'])

        except (KeyError, ValueError):
            raise HTTPBadRequest

        location = Location(latitude=latitude,
                            longitude=longitude)

        mwp = MountainWaveProject.get_info(location)

        mwp_info = []
        for wave in mwp:
            if wave.main_wind_direction:
                if isnumeric(wave.main_wind_direction):
                    wind_direction = wave.main_wind_direction + u"°"
                else:
                    wind_direction = wave.main_wind_direction
            else:
                wind_direction = _("Unknown")

            mwp_info.append(dict(name=wave.name,
                                 main_wind_direction=wind_direction
                                 ))

        return dict(waves=mwp_info)