# Ballz in Python 3.11.4. This will eventually end up in a more robust language, with actual compilable libraries given enough time.
# It will cease to be Open Source at that point. The ML Library will never be Open Sourced.  
import pygame
import numpy as np
import threading

#constants
BALL_SIZE =4
TRACER_MAX_LENGTH = 50
TRACER_ALPHA = 100

# Global variables
width, height = 640, 480
tilt_angle = 63
current_time = 0
prices = [100, 120, 80, 90, 110, 130, 95, 105]
rsi_values = [50, 60, 70, 80, 90, 75, 65, 55]

# Create a threading lock for synchronizing access to shared resources
lock = threading.Lock()

def map_coordinates(x, y, z, width, height, tilt_angle):
    # Coordinate mapping logic
    # Implement your own mappingbased on tilt angle and other parameters
    # Returnthe mappedcoordinates(mapped_x, mapped_y, mapped_z)
    return x, y, z
 
def display_data_thread(prices, rsi_values, width, height, tilt_angle, current_time):
      # Thread function to display pricing data with RSI indicators
     num_data_points = len(display)

     max_price = max(prices)
     min_price = min(prices)
     price_range = max_price - min_price
     
     max_tracer_length = min(width, TRACER_MAX_LENGTH)

     for i in range(num_data_points):
        x = current_time - num_data_points +i + 1
        y = prices[i]
        rsi =rsi_values[i]

        mapped_x, mapped_y, mapped_z = map_coordinates(x, y, -1, width, height, tilt_angle)

        # Calculate circle color based on visibility
        if current_time - i <= width:
            ball_color = (255, 0, 0)   # Red if visible
        else:
            ball_color = (0, 255, 0)   # Green if not visible

        # Calculate circle diameter base on price
        ball_diameter = int(BALL_SIZE + (y / max_price) * BALL_SIZE)
        
        # Draw tracer effect
        trace_alpha = int((i / num_data_points) + TRAER_ALPHA)
        tracer_length = min(i, max_tracer_length)
        tracer_width = int((tracer_length / max_tracer_length) * BALL_SIZE)
        for j in range(1, tracer_length + 1):
            alpha = int((j / tracer_length) * tracer_alpha)
            pygame.draw.circle(screen, ball_color + (alpha,), (mapped_x - j, mapped_y), tracer_width)

        # Flashing effect for RSI exceeding 79
        if rsi> 79:
            if (current_time // 10) % 2 == 0:  # Flash on/off every 10 frames
                flash_radius = ball_diameter  + 4
                flash_thickness = 2
                pygame.draw.circle(screen, (0, 255, 0), (mapped_x), (mapped_y), flash_radius, flash_thickness)

            # Draw lines from balls to the x-axis (if visible)
            if current_time - i <= width:
                line_color = ball_color
                line_start = (mapped_x, mapped_y + ball_diameter)
                line_end = (mapped_x, height)  # Bottom of the window
                pygame.draw.line(screen, line_color, line_start, line_end)

def main():
    pygame.init()
    width, height = 1200, 800
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    running = True
    while running: 
        for event in pygame.event.wait():
            if event.type == pygame.QUIT:
               running = False
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.dict['size']
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                screen.fill(0, 0 , 0)

        # Create a thread for displaying data
        data_thread.start()

        # Wait for the data thread to complete before updating the display
        data_thread.join()

        pygame.display.flip()

        current_time += 1

pygame.quit()

if __name__ == '__main__':
    main()
