from backend.prisma.client import Client

def reset_all_actives():
    print("Resetting all tracks to active...")
    db = Client()
    db.connect()
    db.track.update_many(
        where={
            'active': False
        },
        data={
            'active': True
        }
    )
    db.disconnect()
    print("Done.")

if __name__ == "__main__":
    reset_all_actives()
