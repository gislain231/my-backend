from geopy.distance import great_circle
from typing import Tuple, List, Dict, Optional

def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """Calculate distance between two (lat,lng) points in kilometers"""
    return great_circle(point1, point2).km

def is_within_radius(base_point: Tuple[float, float], 
                    check_point: Tuple[float, float], 
                    radius_km: float) -> bool:
    """Check if a point is within given radius of base point"""
    return calculate_distance(base_point, check_point) <= radius_km

def find_nearest(point: Tuple[float, float], 
                locations: List[Dict], 
                max_distance: Optional[float] = None) -> List[Dict]:
    """
    Find nearest locations to a point
    Args:
        point: (lat, lng) tuple
        locations: List of dicts with 'lat' and 'lng' keys
        max_distance: Optional max distance in km
    Returns:
        List of locations sorted by distance with distance added
    """
    with_distances = []
    for loc in locations:
        if 'lat' not in loc or 'lng' not in loc:
            continue
            
        dist = calculate_distance(point, (loc['lat'], loc['lng']))
        if max_distance is None or dist <= max_distance:
            loc_copy = loc.copy()
            loc_copy['distance_km'] = dist
            with_distances.append(loc_copy)
    
    return sorted(with_distances, key=lambda x: x['distance_km'])