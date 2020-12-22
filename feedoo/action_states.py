class ActionStates:
    def __init__(self, action_class_name, info):
        self._info = info
        self._stats = {
            "name":action_class_name,
            "info":None,
            "in":dict(), # what action receive
            "bypass":dict(), # what is refused by filter "match"
            "do":dict(), # what do action receive
            "ignore":dict(), # what do action ignored or failed events. Ignore must be added in the do function.
            "out":dict() # what action produce (do or update)
        }

    def __getattribute__(self, name):
        if name.startswith("add_"):
            stat_name = name[4:]
            if stat_name not in  object.__getattribute__(self, "_stats") or stat_name in ["name", "info"]:
                raise AttributeError(name)

            def generic_add(event):
                if event is not None:
                    tag = event.tag
                    local_stats = object.__getattribute__(self, "_stats")[stat_name]
                    if tag not in local_stats: 
                        local_stats[tag] = 0
                    local_stats[tag] += 1
                    return local_stats[tag]
                    
            return generic_add

        else:
            return object.__getattribute__(self, name)

    def get_states(self):
        if self._stats["info"] is None:
            self._stats["info"] = self._info()
        return self._stats