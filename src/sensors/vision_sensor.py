from math import atan2, pi

class VisionSensor:
    def __init__(self, player, npcs, bullets, obstacles, items):
        self.player = player
        self.npcs = npcs
        self.bullets = bullets
        self.obstacles = obstacles
        self.items = items

    def get_all_objects(self):
        return [self.player] + self.npcs + self.bullets + self.obstacles + self.items


    def get_reading(self, character):
        # Potentially visible objects
        # TODO currently not processing very large objects in front of the sensor
        objects_in_fov = [x for x in self.get_all_objects()
                          if character.pos.distance_to(x.pos) <= x.radius + character.vision_radius
                          and -character.vision_angle / 2 < character.dir.angle_to(x.pos - character.pos) < character.vision_angle / 2
                          and x.id != character.id]

        objects_in_fov.sort(key=lambda x: character.pos.distance_to(x.pos))
        # Sorted list of objects blocking the view, each is an arc segment (r, l)
        # r < l since we rotate counterclockwise
        # Sorry for counterintuitive naming
        obstructions = []
        visible_objects = []
        for obj in objects_in_fov:
            obj_m = character.dir.angle_to(obj.pos - character.pos)
            alpha = atan2(obj.radius, character.pos.distance_to(obj.pos)) / pi * 180
            obj_l, obj_r = obj_m + alpha, obj_m - alpha
            is_obstructed = False

            for i, segment in enumerate(obstructions):
                r, l = segment
                # Obstruction is before the object
                while obj_r > l:
                    continue

                # A new disjoint segment
                if obj_l < r:
                    obstructions.insert(i, (obj_r, obj_l))
                    break

                if obj_r < r:
                    # Segment overlaps with the next one (or more)
                    # Merge all of them together
                    last_overlapping = i
                    while last_overlapping < len(obstructions) - 1 and obstructions[last_overlapping + 1][0] < obj_l:
                        last_overlapping += 1

                    new_l = max(obj_l, obstructions[last_overlapping][1])
                    for j in range(last_overlapping, i, -1):
                        obstructions.pop(j)
                    obstructions[i] = (obj_r, new_l)
                    break


                if obj_l <= l:
                    # Object is behind the obstruction
                    is_obstructed = True
                    break

                # Segment overlaps from the with the next one (or more)
                # Merge them
                last_overlapping = i
                while last_overlapping < len(obstructions) - 1 and obstructions[last_overlapping + 1][0] < obj_l:
                    last_overlapping += 1

                new_l = max(obj_l, obstructions[last_overlapping][1])
                for j in range(last_overlapping, i, -1):
                    obstructions.pop(j)
                obstructions[i] = (r, new_l)
                break

            if is_obstructed:
                continue

            visible_objects.append(obj)

        return visible_objects