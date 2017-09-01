from point import point, boundary
from ball import ball
import constants

def detect_collisions(balls, canvas):
    collisions = []
    for ball in balls:
        pos = canvas.coords(ball.representation)
        for ball2 in balls:
            collision_identifier=[min(ball.id_number, ball2.id_number), max(ball.id_number, ball2.id_number)]
            if ball.id_number != ball2.id_number and collision_identifier not in collisions:

                pos2 = canvas.coords(ball2.representation)
                collision = False
                # Left less than right
                if ( pos2[0] <= pos[2] and 
                     pos2[2] >= pos[0] and
                     pos2[1] <= pos[3] and 
                     pos2[3] >= pos[1]):
                    collision = True

                if collision:
                    collisions.append(collision_identifier)
                    print str(ball.id_number) + " hit " + str(ball2.id_number)
                    # velocity decomposed along axes
                    print "Initial velocity: " + str(ball.velocity)
                    energy = (
                        (ball.velocity * ball.mass) + 
                        (ball2.velocity * ball.mass) )
                    print energy

                    mass = ball.mass + ball2.mass

                    ball.velocity = energy * ball.mass / mass
                    ball2.velocity = energy * ball2.mass / mass

                    if ball.frozen is not True:
                        dx=0
                        while(ball.get_boundaries().circles_hit(ball2.get_boundaries())):
                            if ball.get_boundaries().is_left_of(ball2.get_boundaries()):
                                canvas.move(ball.representation,-1,0)
                                dx-=1
                            else:
                                canvas.move(ball.representation,1,0)
                                dx+=1
                        canvas.move(ball.representation, ball.velocity.x, ball.velocity.y)
                        ball.velocity.x+=dx
                    
                    if ball2.frozen is not True:
                        dx=0
                        while(ball.get_boundaries().circles_hit(ball2.get_boundaries())):
                            if ball.get_boundaries().is_left_of(ball2.get_boundaries()):
                                canvas.move(ball2.representation,1,0)
                                dx+=1
                            else:
                                canvas.move(ball2.representation,-1,0)
                                dx-=1
                        canvas.move(ball2.representation, ball2.velocity.x, ball2.velocity.y)
                        ball2.velocity.x+=dx
                    canvas.update()

                    print "Ball1 Resultant velocity: " + str(ball.velocity)
                    print "Ball2 Resultant velocity: " + str(ball2.velocity)
                    
