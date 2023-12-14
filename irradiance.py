"""Compute the irradiance received on a horyzontal surface.
"""

import time

import numpy as np
import pandas as pd
import datetime as dt


def get_irradiance(latitude, longitude, unix_timestamp):
    """Compute the irradiance without atmosphere given the latitude,
    longitude and unix timestamp.
    Args:
        latitude (int): latitude (in °) of location. ]-65°, 65°[
        longitude (int): longitude (in °) of location. ]-180°, 180°[
        unix_timestamp (int): unix timestamp (in s)
    Return:
    	irradiance (float): irradiance (in W/m2): Irradiance received without the atmosphere.
    """
    # Convert latitude (°) to 
    phi = latitude*np.pi/180
    
    # Extract local datetime based on longitude and unix_timestamp
    conversion_degree_to_seconds = 3600/15
    unix_timestamp_local = unix_timestamp + longitude*conversion_degree_to_seconds
    datetime = dt.datetime.utcfromtimestamp(unix_timestamp_local)
    
    # Extract day of year and time of day.
    n = datetime.timetuple().tm_yday
    hour = datetime.hour + datetime.minute/60
    omega = 15*(hour - 12)*np.pi/180
    # Compute
    return compute_I_oh_(n, compute_cos_theta_z_(compute_delta_(n), omega, phi)) 


################################################################################################################################


def compute_I_oh_(n, cos_theta_z):
    """Compute the irradiance outside the atmosphere on a place horizontal to the Earth's surface.
    Args:
        n (int): day of the year. [1:365]
        cos_theta_z (no unit): cosinus of the solar zenith angle, describing the height of the sun in the sky.
    Return:
        I_oh (float): Computed irradiance (W.m-2).
    """
    return compute_I_o_(n)*cos_theta_z


def compute_cos_theta_z_(delta, omega, phi):
    """Compute the cosinus of the zenith angle of an observer.
    Args:
        delta (radian): declination angle. 
        omega (radian): hour angle (i.e time of the day).
        phi (radian): latitude of the point.
    Return:
        cos_theta_z (no unit): cosinus of the solar zenith angle.
    """
    if delta < -0.41 or delta > 0.41:
        raise ValueError(f"The given declination angle should be between \
            -0.41 Rad (-23.45°) and 0.41 Rad (23.45°), {delta} Rad given.")
    if omega < -np.pi or omega > np.pi:
        raise ValueError(f"The given hour angle omega should be between \
            -3.142 (-pi Rad) and 3.142 (pi Rad), {omega} Rad given.")
    if phi < -np.pi/2 or phi > np.pi/2:
        raise ValueError(f"The given latitude phi should be between \
            -1.57 Rad (-pi/2 Rad) and 1.57 Rad (pi/2 Rad), {phi} Rad given.")
    
    # Compute the sunset and sunrise time
    omega_s = compute_omega_s_(delta, phi)
    
    # Return values based on the hour angle compared to the sunset and sunrise time
    if -omega_s < omega < omega_s:
        return np.sin(delta)*np.sin(phi) + np.cos(delta)*np.cos(phi)*np.cos(omega)
    else: return 0


def compute_delta_(n):
    """Compute the declination angle.
    Args:
        m (int): day of the year.
    Return:
        delta (radian): Angle between the equatorial plane and a line joining the centres ofthe Sun and the Earth.
    """
    if n < 1 or n > 366:
        raise ValueError(f"The given day of the year n should be between 1 and 366, {n} given.")
    return 23.45*np.pi/180*np.sin(2*np.pi*(284 + n)/365.25)


################################################################################################################################


def compute_I_o_(n):
    """Compute the irradiance outside the atmosphere on a plane perpendicular to the Sun's rays.
    Args:
        n (int): day of the year. [1:365]
    Return:
        I_o (float): Computed irradiance (W.m-2).
    """
    I_sc = 1367
    if n < 1 or n > 366:
        raise ValueError(f"The given day of the year n should be between 1 and 366, {n} given.")
    return I_sc*(1 + 0.034*np.cos(2*np.pi*n/365.25))


def compute_omega_s_(delta, phi):
    """Compute the sunset (= -sunrise) angle for horizontal plane.
    Args:
        delta (radian): declination angle.
        phi (radian): latitude of the point.
    Return:
        omega_s (radian): sunset angle.
    """
    if delta < -0.41 or delta > 0.41:
        raise ValueError(f"The given declination angle should be between \
            -0.41 Rad (-23.45°) and 0.41 Rad (23.45°), {delta} Rad given.")
    if phi < -np.pi/2 or phi > np.pi/2:
        raise ValueError(f"The given latitude phi should be between \
            -1.57 Rad (-pi/2 Rad) and 1.57 Rad (pi/2 Rad), {phi} Rad given.")
    return np.arccos(-np.tan(phi)*np.tan(delta))


################################################################################################################################