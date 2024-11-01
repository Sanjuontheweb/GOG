    # actually creating the beam
    if keys[pygame.K_UP]:
        # Create a new projectile and add it to the beams list
        new_proje = Projectile(round(movee.rect.centerx), round(movee.rect.centery), 1)
        beams.append(new_proje)

    # moving of the beam
    beams_del = []    # the beams to remove
    for beam in beams:
            beam.y -= beam.vel
            if beam.y < 0:
                beams_del.append(beam)

    # beams to remove which are out of screen
    for beam in beams_del:
        beams.remove(beam)

    # drawing the beam
    for beam in beams:
        beam.draw()