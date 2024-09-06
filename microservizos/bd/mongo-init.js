db.createUser(
        {
            user: "user",
            pwd: "1234",
            roles: [
                {
                    role: "readWrite",
                    db: "test"
                }
            ]
        }
);
