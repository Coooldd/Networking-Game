from networking_objects.client.client_game_functionality import ClientGameFunctionality


game = ClientGameFunctionality('10.137.135.192')
game.start_game_loop() # initializes the network, threads, starts game loop
