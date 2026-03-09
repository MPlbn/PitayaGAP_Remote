CXX = g++

CFLAGS  = -Wall -std=c++20 ## -Werror
CFLAGS += -I/opt/redpitaya/include
CFLAGS += -I/opt/redpitaya/include/api250-12

LDFLAGS = -L/opt/redpitaya/lib

LDLIBS = -static -lrp-hw-can -lrp -lrp-hw-calib -lrp-hw-profiles
LDLIBS += -lrp-gpio -lrp-i2c
LDLIBS += -lrp-hw -lm -lstdc++ -lpthread -li2c -lsocketcan

# List of programs to compile
TARGET = custom_server

# Source directory
SRCDIR = src
SRCS = $(SRCDIR)/pitaya_gen_acq_server.cpp $(SRCDIR)/serverUtils.cpp
OBJS := $(SRCS:.cpp=.o)

all: $(TARGET)

# Link
$(TARGET): $(OBJS)
	$(CXX) $(CFLAGS) $(LDFLAGS) $(OBJS) $(LDLIBS) -o $@

# Compile sources to objects
$(SRCDIR)/%.o: $(SRCDIR)/%.cpp
	$(CXX) $(CFLAGS) -c $< -o $@

clean:
	$(RM) $(OBJS)
	$(RM) $(TARGET)
