from helper import find_age_from_dob,convert_str_to_datetime

class Player:

    def __init__(self,player_id,name,dob=None):
        self.player_id=player_id
        self.player_name=name
        self.dob=convert_str_to_datetime(dob) if isinstance(dob,str) else dob
        self.age=None if not self.dob else find_age_from_dob(self.dob)
        self.games_played={}
        self.total_games_played=0
        self.games_abandoned=0

    def __str__(self) -> str:
        return f"ID={self.player_id}, Name={self.player_name}, DateOfBirth={self.dob}"

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}(player_id={self.player_id!r}, player_name={self.player_name!r}, dob={self.dob!r})"

       