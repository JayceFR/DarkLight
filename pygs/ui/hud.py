import pygame
class Hud():
    def __init__(self, obj) -> None:
        pygame.init()
        self.joysticks = {}
        self.obj = obj
        self.return_dict = {"l_click": False, "ongrid": True, "r_click": False, "run" : True, "left" : False, "right" : False, "up" : False, "down": False, "jump": False, "x_axis" : 0.0, "y_axis" : 0.0}

    def events(self, key_controls):
        # self.return_dict = {"run" : True, "left" : False, "right" : False, "jump": False}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.return_dict["run"] = False
            if event.type == pygame.JOYBUTTONDOWN:
                joystick = self.joysticks[event.instance_id]
                if event.button == 9 or event.button == 10:
                    if self.obj.__class__.__name__ == "Game" and self.obj.dead <= 0:
                        self.obj.player.dash(joystick)
                        # joystick.rumble(0, 0.6, 200)
                if event.button == 2:
                    if self.obj.__class__.__name__ == "Game":
                        self.obj.player.attack()
                if event.button == 0:
                    joystick = self.joysticks[event.instance_id]
                    self.return_dict["jump"] = True
                    if self.obj.__class__.__name__ == "Game" and not self.obj.settings_window:
                        if self.obj.dead <= 0:
                            if self.obj.player.jumps and not self.obj.player.jump_buffer:
                                self.obj.player.jump()
                            else:
                                self.obj.player.jump_buffer = 14
                    # if joystick.rumble(0, 0.7, 500):
                    #     print(f"Rumble effect played on joystick {event.instance_id}")
            if event.type == pygame.JOYBUTTONUP:
                if event.button == 0:
                    self.return_dict["jump"] = False
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 4 or event.axis == 5:
                    if event.value > 0.3:
                        joystick = self.joysticks[event.instance_id]
                        if self.obj.__class__.__name__ == "Game" and self.obj.dead <= 0:
                            self.obj.player.dash(joystick)
                            # joystick.rumble(0, 0.6, 200)
                if event.axis == 0:
                    self.return_dict["left"] = False
                    self.return_dict["right"] = False
                    self.return_dict["x_axis"] = event.value
                    if event.value < -0.3:
                        self.return_dict["left"] = True
                    if event.value > 0.3:
                        self.return_dict["right"] = True
                if event.axis == 1:
                    self.return_dict["up"] = False
                    self.return_dict["down"] = False
                    self.return_dict["y_axis"] = event.value
                    if event.value < -0.3:
                        self.return_dict["up"] = True
                    if event.value > 0.3:
                        self.return_dict["down"] = True
            if event.type == pygame.JOYDEVICEADDED:
                print(event)
                joy = pygame.joystick.Joystick(event.device_index)
                self.joysticks[joy.get_instance_id()] = joy
                print(str(joy.get_instance_id()) + " Connected ")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.return_dict["l_click"] = True
                    if self.obj.__class__.__name__ == "Editor":
                        if not pygame.rect.Rect(0,0,100,600).collidepoint(self.obj.mouse_pos) and not self.obj.ongrid:
                            self.obj.toggle_offgrid()
                if event.button == 3:   
                    self.return_dict["r_click"] = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.return_dict["l_click"] = False
                if event.button == 3:
                    self.return_dict["r_click"] = False

            #Keyboard controls
            
            if event.type == pygame.KEYDOWN:
                if event.key in key_controls["right"]:
                    self.return_dict["right"] = True
                if event.key in key_controls["left"]:
                    self.return_dict["left"] = True
                if event.key in key_controls["jump"]:
                    if self.obj.__class__.__name__ == "Game" and not self.obj.settings_window:
                        if self.obj.dead <= 0:
                            if self.obj.player.jumps and not self.obj.player.jump_buffer:
                                self.obj.player.jump()
                            else:
                                self.obj.player.jump_buffer = 14
                    self.return_dict["jump"] = True
                if event.key in key_controls["dash"]:
                    if self.obj.__class__.__name__ == "Game" and self.obj.dead <= 0:
                        self.obj.player.dash()
                if event.key in key_controls["pickup"]:
                    if self.obj.__class__.__name__ == "Game":
                        if self.obj.player.who == "j":
                            self.obj.player.update_who("h")
                        else:
                            self.obj.player.update_who("j")
                        # if self.obj.collected == False:
                        #     if self.obj.player.rect().collidepoint(self.obj.buried_point[0], self.obj.buried_point[1]):
                        #         self.obj.sfx['pickup'].play()
                if event.key in key_controls["select"]:
                    if self.obj.__class__.__name__ == "Game" and self.obj.settings_window and self.obj.settings.curr_hover_pos != -1:
                        self.obj.settings.update_res(self.obj.settings.resolutions[self.obj.settings.curr_hover_pos][1])
                if event.key in key_controls["up"]:
                    if self.obj.__class__.__name__ == "Game" and self.obj.settings_window:
                        self.obj.settings.update_hover_pos(-1)
                    else:
                        self.return_dict["up"] = True
                if event.key in key_controls["down"]:
                    if self.obj.__class__.__name__ == "Game" and self.obj.settings_window:
                        self.obj.settings.update_hover_pos(1)
                    self.return_dict["down"] = True
                if event.key == pygame.K_LSHIFT:
                    if self.obj.__class__.__name__ == "Editor":
                        self.return_dict['ongrid'] = not self.return_dict['ongrid']
                if event.key in key_controls["attack"]:
                    if self.obj.__class__.__name__ == "Game":
                        self.obj.player.attack()
                if event.key in key_controls["settings"]:
                    if self.obj.__class__.__name__ == "Game":
                        self.obj.settings_window = not self.obj.settings_window
                if event.key == pygame.K_o:
                    if self.obj.__class__.__name__ == "Editor":
                        self.obj.tilemap.save(self.obj.path)
                if event.key == pygame.K_t:
                    if self.obj.__class__.__name__ == "Editor":
                        self.obj.tilemap.autotile()
                if event.key == pygame.K_TAB:
                    if self.obj.__class__.__name__ == "Game" and self.obj.settings_window:
                        self.obj.settings.update_tab_hover_pos()
            if event.type == pygame.KEYUP:
                if event.key in key_controls["right"]:
                    self.return_dict["right"] = False
                if event.key in key_controls["left"]:
                    self.return_dict["left"] = False
                if event.key == key_controls["jump"]:
                    self.return_dict["jump"] = False
                if event.key in key_controls["up"]:
                    self.return_dict["up"] = False
                if event.key in key_controls["down"]:
                    self.return_dict["down"] = False
    
    def get_controls(self):
        return self.return_dict