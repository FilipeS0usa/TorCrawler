from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Create model LargeContent 
class LargeContent(Base):
    __tablename__ = "large_content"

    id = Column(Integer, primary_key=True, autoincrement=True)
    header = Column(Text)


# Create model file
class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    original_name = Column(Text, nullable=False)
    type_of_file = Column(String(50), nullable=False)


# Create model hash
class Hash(Base):
    __tablename__ = "hash"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hash = Column(String(100), nullable=False)

# Create model protocol 
# TODO: check how to implement UNIQUE 
class Protocol(Base):
    __tablename__ = "protocol"

    id = Column(Integer, primary_key=True, autoincrement=True)
    protocol = Column(String(10), nullable=False)


# Create model Path 
class Path(Base):
    __tablename__ = "path"

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(Text, nullable=False)
    date_last_scan = Column(DateTime)
    date_creation = Column(DateTime, nullable=False)
    disabled = Column(Boolean, nullable=False)
    tries = Column(Integer, nullable=False)
    large = Column(Boolean, nullable=False)
    file = Column(Boolean, nullable=False)
    file_id = Column(
        Integer,
        ForeignKey("file.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    hash_id = Column(
        Integer,
        ForeignKey("hash.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    large_content_id = Column(
        Integer,
        ForeignKey("large_content.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )

    # TODO: review how I would implement this. I think I can use this names for 
    # variables
    file = relationship("File", back_populates="path")
    hash = relationship("Hash", back_populates="path")
    large_content = relationship("LargeContent", back_populates="path")

    def new_link(self, link_url):
        """
        Populate the new link with the respective values
        :param link_url:
        :return:
        """
        date_time = datetime.today()
        self.link = link_url
        self.date_discovery = date_time
        self.disabled = 0
        self.tries = 0
        self.large = 0

    def update_last_scan(self):
        """
        Update last scan date
        :param:
        :return:
        """
        date_time = datetime.today()
        self.date_last_scan = date_time

    def disable_link(self):
        """
        Disable the link
        :param:
        :return:
        """
        date_time = datetime.today()
        self.disabled = 1
        self.date_last_scan = date_time

    def add_tries(self):
        """
        add_tries to the object
        :return:
        """
        self.tries += 1

# Create model Hostname
class Hostname(Base):
    __tablename__ = "hostname"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(Text, nullable=False)
    date_last_scan = Column(DateTime)
    date_creation = Column(DateTime)
    disabled = Column(Boolean, nullable=False)
    protocol_id = Column(
        Integer,
        ForeignKey("protocol.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    path_id = Column(
        Integer,
        ForeignKey("path.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )

    protocol = relationship("Protocol", back_populates="hostname")
    path = relationship("Path", back_populates="hostname")

    def update_last_scan(self):
        date_time = datetime.today()
        self.date_last_scan = date_time


# TODO: Study better how I would do the relationships.
